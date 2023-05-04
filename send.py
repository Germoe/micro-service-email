from gmail import Gmail

def send(provider, subject, body, to, body_type='html'):
    if provider == 'gmail':
        gmail = Gmail()
        return gmail.send(to, subject, body, body_type)
    else:
        print(f'Provider {provider} is not supported')
        return False
    return True