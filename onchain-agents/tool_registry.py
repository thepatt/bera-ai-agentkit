import re
from blockchain_utils import get_balance, get_transaction

# Create a registry to support thousands of tools
tool_registry = []


def register_tool(keywords):
    def decorator(func):
        tool_registry.append((keywords, func))
        return func

    return decorator


@register_tool(["balance"])
def tool_get_balance(prompt):
    address_match = re.search(r"0x[a-fA-F0-9]{40}", prompt)
    if address_match:
        address = address_match.group(0)
        return get_balance(address)
    else:
        return "No valid Ethereum address found."


@register_tool(["transaction"])
def tool_get_transaction(prompt):
    tx_hash_match = re.search(r"0x[a-fA-F0-9]{64}", prompt)
    if tx_hash_match:
        tx_hash = tx_hash_match.group(0)
        return get_transaction(tx_hash)
    else:
        return "No valid transaction hash found."


def determine_action(prompt):
    lower_prompt = prompt.lower()
    matching_responses = [
        tool_func(prompt)
        for keywords, tool_func in tool_registry
        if any(keyword in lower_prompt for keyword in keywords)
    ]
    return "\n".join(matching_responses) if matching_responses else None
