from werkzeug.security import generate_password_hash

# List of passwords to hash
passwords = ['betsythefish', 'raikathebird', 'aishathedog', 'ericthemonkey', 'mishathebug', 'chenthegoat', 'gwenthecat','parththepig','alexthecow','maddiethebear','charliethekangaroo','priyoshithechicken','liamtherat','minathepenguin']

# Generate and print hashed passwords
for password in passwords:
    hashed_password = generate_password_hash(password)
    print(f'Password: {password}, Hash: {hashed_password}')