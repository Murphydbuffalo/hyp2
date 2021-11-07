from django.test import TestCase
from django.core.exceptions import ValidationError
from hyp.models import HypUser, IdempotencyKey


class TestIdempotencyKey(TestCase):
    my_list = []

    def anExampleFunction(self, number1, number2, *moreNumbers):
        self.my_list.append(number1)
        self.my_list.append(number2)

        for num in moreNumbers:
            self.my_list.append(num)

        return self.my_list

    def test_instance_method_idempotency(self):
        self.assertEqual(IdempotencyKey.objects.count(), 0)
        self.assertEqual(self.my_list, [])

        IdempotencyKey.call_once(
            func=lambda: self.anExampleFunction(1, 2, 3),
            key="some key",
        )

        self.assertEqual(self.my_list, [1, 2, 3])
        self.assertEqual(IdempotencyKey.objects.count(), 1)

        IdempotencyKey.call_once(
            func=lambda: self.anExampleFunction(4, 5, 6),
            key="some key",
        )

        self.assertEqual(self.my_list, [1, 2, 3])
        self.assertEqual(IdempotencyKey.objects.count(), 1)

        IdempotencyKey.call_once(
            func=lambda: self.anExampleFunction(4, 5, 6),
            key="a different key",
        )

        self.assertEqual(self.my_list, [1, 2, 3, 4, 5, 6])
        self.assertEqual(IdempotencyKey.objects.count(), 2)

        IdempotencyKey.call_once(
            func=lambda: self.anExampleFunction(number1=7, number2=8),
            key="a third key",
        )

        self.assertEqual(self.my_list, [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(IdempotencyKey.objects.count(), 3)

    def test_no_key(self):
        self.my_list = []

        IdempotencyKey.call_once(
            func=lambda: self.anExampleFunction(1, 2, 3),
            key=None,
        )

        IdempotencyKey.call_once(
            func=lambda: self.anExampleFunction(4, 5, 6),
            key=None,
        )

        self.assertEqual(self.my_list, [1, 2, 3, 4, 5, 6])
        self.assertEqual(IdempotencyKey.objects.count(), 0)

    def returnTrue(self):
        return True

    def test_return_value(self):
        result = IdempotencyKey.call_once(func=self.returnTrue, key="foo")
        self.assertEqual(True, result)

    # Try to create a pair of users where we simulate one being invalid
    # The idempotency key should perform this work in a transaction,
    # meaning neither gets created
    def problematicDatabaseWrites(self):
        HypUser(email="averyniceguy@example.com", username="averyniceguy@example.com", password="thisisareallyverynicepasswordindeed").save()
        HypUser(email="anotherveryniceguy", username="anotherveryniceguy", password="wowthisissuchagreatpasswordsoterrfic").save()
        raise ValidationError("These users smell funny")

    def goodDatabaseWrites(self):
        HypUser(email="averyniceguy@example.com", username="averyniceguy@example.com", password="thisisareallyverynicepasswordindeed").save()
        HypUser(email="anotherveryniceguy", username="anotherveryniceguy", password="wowthisissuchagreatpasswordsoterrfic").save()


    def test_idempotency_with_database_transaction(self):
        self.assertEqual(HypUser.objects.count(), 0)
        self.assertEqual(IdempotencyKey.objects.count(), 0)

        try:
            IdempotencyKey.call_once(func=self.problematicDatabaseWrites, key ="create user")
        except(ValidationError):
            self.assertEqual(HypUser.objects.count(), 0)
            self.assertEqual(IdempotencyKey.objects.count(), 0)

        IdempotencyKey.call_once(func=self.goodDatabaseWrites, key ="create user")

        self.assertEqual(HypUser.objects.count(), 2)
        self.assertEqual(IdempotencyKey.objects.count(), 1)

        IdempotencyKey.call_once(func=self.goodDatabaseWrites, key ="create user")

        self.assertEqual(HypUser.objects.count(), 2)
        self.assertEqual(IdempotencyKey.objects.count(), 1)
