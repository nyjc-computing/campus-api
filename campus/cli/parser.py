# Handles parsing of the BNF-defined syntax
class CLIParser:
    def parse(self, command: str):
        parts = command.split()
        result = {
            'resource_chain': [],
            'id': None,
            'action': None,
            'args': []
        }

        for part in parts:
            if part in ["clients", "applications", "users", "circles", "apikeys", "emailotp", "sources", "members", "profile"]:
                result['resource_chain'].append(part)
            elif part in ["get", "new", "update", "delete", "approve", "reject", "revoke", "request", "verify", "add", "remove", "reparent"]:
                result['action'] = part
            elif part.startswith("--") or part.startswith("-"):
                result['args'].append(part)
            else:
                result['id'] = part

        return result