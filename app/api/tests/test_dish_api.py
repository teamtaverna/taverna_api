from django.test import Client, TestCase

from .utils import create_admin_account, make_request


class DishApiTest(TestCase):
    """Test for Dish API"""

    def setUp(self):
        self.client = Client()
        create_admin_account()
        self.data = {
            'name': 'rice',
            'description': 'white rice'
        }
        self.dishes = (
            ('rice', 'white rice'),
            ('Coconut rice', 'rice with coconut flavor'),
            ('plantain', 'fried plantain'),
        )

    def create_dish(self, name, description):
        query = '''
            mutation{
              createDish(input: {name: "%s", description: "%s"}){
                dish{
                  id,
                  originalId,
                  name
                }
              }
            }
        ''' % (name, description)

        return make_request(self.client, query, 'POST')

    def create_multiple_dishes(self):
        return [self.create_dish(name, description) for name, description in self.dishes]

    def retrieve_dish(self, id):
        query = 'query {dish(id: "%s" ) {name}}' % (id)

        return make_request(self.client, query)

    def ordering_test_helper(self, ordering_param, records):
        # For ascending ordering
        query = 'query{dishes(order_by: "%s") {edges{node{name}}}}' % (ordering_param)
        expected = {
            'dishes': [
                {
                    'name': records[0]
                },
                {
                    'name': records[1]
                },
                {
                    'name': records[2]
                }
            ]
        }
        response = make_request(self.client, query)
        self.assertEqual(expected, response)

        # For descending ordering
        query = 'query {dishes(order_by: "-%s") {edges{node{name}}}}' % (ordering_param)
        expected['dishes'].reverse()
        response = make_request(self.client, query)
        self.assertEqual(expected, response)

    def test_creation_of_dish_object(self):
        # For new dish record
        response = self.create_dish(self.data['name'], self.data['description'])
        created_dish = response['dish']
        expected = {
            'dish': {
                'id': created_dish['id'],
                'originalId': created_dish['originalId'],
                'name': self.data['name']
            }
        }
        self.assertEqual(expected, response)

        # For existing weekday record
        response = self.create_dish(self.data['name'], self.data['description'])
        self.assertEqual({'dish': None}, response)

    def test_retrieval_of_one_dish_object(self):
        # Retrieve with valid id
        expected = {
            'dish': {
                'name': self.data['name']
            }
        }
        create_response = self.create_dish(self.data['name'], self.data['description'])
        response = self.retrieve_dish(create_response['dish']['id'])
        self.assertEqual(expected, response)

        # Retrieve with invalid id
        self.assertEqual({'dish': None}, self.retrieve_dish(2))

    def test_retrieval_of_multiple_dish_objects_without_filtering(self):
        self.create_multiple_dishes()

        query = 'query {dishes{edges{node{name}}}}'

        expected = {
            'dishes': [
                {
                    'name': self.dishes[0][0]
                },
                {
                    'name': self.dishes[1][0]
                },
                {
                    'name': self.dishes[2][0]
                }
            ]
        }

        response = make_request(self.client, query)

        self.assertEqual(expected, response)

    def test_retrieval_of_multiple_user_objects_filter_by_username(self):
        self.create_multiple_dishes()
        query = 'query {dishes(name_Icontains: "Rice") {edges{node{name}}}}'

        expected = {
            'dishes': [
                {
                    'name': self.dishes[0][0]
                },
                {
                    'name': self.dishes[1][0]
                }
            ]
        }

        response = make_request(self.client, query)

        self.assertEqual(expected, response)

    def test_retrieval_of_multiple_dish_objects_ordering_by_id(self):
        self.create_multiple_dishes()
        records = [
            self.dishes[0][0],
            self.dishes[1][0],
            self.dishes[2][0]
        ]

        self.ordering_test_helper('id', records)

    def test_retrieval_of_multiple_dish_objects_ordering_by_name(self):
        self.create_multiple_dishes()
        records = [
            self.dishes[1][0],
            self.dishes[2][0],
            self.dishes[0][0]
        ]

        self.ordering_test_helper('name', records)

    def test_update_of_dish_object(self):
        # Update with valid id
        create_response = self.create_dish(self.data['name'], self.data['description'])
        query = '''
            mutation{
                updateDish(
                    input: {
                        id: "%s",
                        name: "rice edited"
                    }
                )
                {
                    dish{
                        id,
                        name
                    }
                }
            }
        ''' % (create_response['dish']['id'])
        expected = {
            'dish': {
                'id': create_response['dish']['id'],
                'name': 'rice edited'
            }
        }
        response = make_request(self.client, query, 'POST')
        self.assertEqual(expected, response)

        # Update with invalid id
        query = '''
            mutation{
                updateDish(
                    input: {
                        id: "%s",
                        name: "rice edited"
                    }
                )
                {
                    dish{
                        id,
                        name
                    }
                }
            }
        ''' % ('wrong-id')
        self.assertEqual({'dish': None}, make_request(self.client, query, 'POST'))

    def test_deletion_of_dish_object(self):
        # Delete with valid id
        create_response = self.create_dish(self.data['name'], self.data['description'])
        query = '''
            mutation{
                deleteDish(input: {id: "%s"}){
                    dish{
                        name
                    }
                }
            }
        ''' % (create_response['dish']['id'])
        expected = {
            'dish': {
                'name': self.data['name']
            }
        }
        response = make_request(self.client, query, 'POST')
        self.assertEqual(expected, response)
        self.assertEqual({'dish': None}, self.retrieve_dish(create_response['dish']['id']))

        # Delete with invalid id
        query = '''
            mutation{
                deleteDish(input: {id: "%s"}){
                    dish{
                        name
                    }
                }
            }
        ''' % ('wrong-id')
        self.assertEqual({'dish': None}, make_request(self.client, query, 'POST'))
