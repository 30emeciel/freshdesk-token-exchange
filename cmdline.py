
if __name__ == "__main__":
    # export GOOGLE_APPLICATION_CREDENTIALS="trentiemeciel.json"
    # get the token using postman
    from dotenv import load_dotenv
    load_dotenv()
    import main

    freshdesk_token = main.convert_auth0_token_to_freshdesk_token("gtxiNvJMjuDGec7GUziM2qSupsnCu74I")
    print(f"freshdesk_token: {freshdesk_token}")
