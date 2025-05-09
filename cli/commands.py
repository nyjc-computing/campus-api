# Contains logic for executing commands
class CommandExecutor:
    def execute(self, parsed_command):
        resource_chain = parsed_command.get('resource_chain', [])
        action = parsed_command.get('action')
        args = parsed_command.get('args', [])
        resource_id = parsed_command.get('id')

        if not resource_chain or not action:
            print("Invalid command")
            return

        # Example: Handle 'clients' resource
        if resource_chain[0] == "clients":
            from resources.clients import ClientsResource
            resource = ClientsResource()
            result = resource.handle(action, {'id': resource_id, 'args': args})
            print(result)
        else:
            print(f"Unknown resource: {resource_chain[0]}")

    def start(self):
        print("Starting...")

    def stop(self):
        print("Stopping...")