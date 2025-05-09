import requests

# Logic for handling 'clients' resource
class ClientsResource:
    def handle(self, action, args):
        # Handle different actions for 'clients' resource
        if action == 'create':
            return self.create_client(args)
        elif action == 'update':
            return self.update_client(args)
        elif action == 'delete':
            return self.delete_client(args)
        elif action == 'get':
            return self.get_client(args)
        else:
            raise ValueError(f"Unknown action: {action}")

    def create_client(self, args):
        url = f"/clients"
        response = requests.post(url, json=args)
        return response.json()

    def update_client(self, args):
        client_id = args.get('id')
        url = f"/clients/{client_id}"
        response = requests.put(url, json=args)
        return response.json()

    def delete_client(self, args):
        client_id = args.get('id')
        url = f"/clients/{client_id}"
        response = requests.delete(url)
        return response.status_code

    def get_client(self, args):
        client_id = args.get('id')
        url = f"/clients/{client_id}" if client_id else "/clients"
        response = requests.get(url)
        return response.json()