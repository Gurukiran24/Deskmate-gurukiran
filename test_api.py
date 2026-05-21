import sys
sys.path.append('inference')

from api.app import detect_intent, execute_tool

# Test intent detection
tests = [
    ('check my software access', 'check_software_access'),
    ('create a ticket for email', 'create_ticket'),
    ('check vpn status', 'check_vpn_status'),
    ('I need a password reset', 'reset_password'),
    ('who is John?', 'get_user_info'),
    ('check ticket T1001', 'get_ticket_status'),
]

print('=== Intent Detection Tests ===')
for msg, expected_tool in tests:
    intent = detect_intent(msg)
    status = 'PASS' if intent['tool'] == expected_tool else 'FAIL'
    print(f'{status}: "{msg}" -> {intent["tool"]} (expected: {expected_tool})')

print()
print('=== Tool Execution Tests ===')
result = execute_tool('check_software_access', '', 'John')
print(f'check_software_access(John): {result}')

result = execute_tool('check_vpn_status', '', 'Alice')
print(f'check_vpn_status(Alice): {result}')

result = execute_tool('reset_password', '', 'Bob')
print(f'reset_password(Bob): {result}')

result = execute_tool('create_ticket', 'email issue', 'Alice')
print(f'create_ticket(Alice, email issue): {result}')

result = execute_tool('get_ticket_status', 'T1001', None)
print(f'get_ticket_status(T1001): {result}')