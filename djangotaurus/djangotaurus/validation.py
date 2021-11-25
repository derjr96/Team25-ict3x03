import re
from datetime import date, datetime


class Validation():
    @staticmethod
    def validate_text(text) -> bool:
        """
            Function to check text type and if it meets the requirement of the regex of
            not having numbers or special characters

            @params: text, the input text
            @returns: bool, True if valid text else false
        """
        text_regex = r"([a-zA-Z]+\s)*[a-zA-Z]{2,45}$"
        if re.match(text_regex, text):
            return True
        return False

    @staticmethod
    def validate_email(email) -> bool:
        """
            Function to check email type and if it meets the requirement of the regex

            @params: email, the input email
            @returns: bool, True if valid email else false
        """
        email_regex = r"(([a-z0-9!#$%&'*+/=?^_`{|}~-]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
        if re.match(email_regex, email):
            return True
        return False

    @staticmethod
    def validate_password(password) -> bool:
        """
            Function to check password type and if it meets the requirement of the regex with a length of 512 characters
            and contains alphabets and numbers only.

            @params: password, the input password
            @returns: bool, True if valid password else false
        """
        password_regex = r"[a-zA-Z0-9]{512}$"
        if re.match(password_regex, password):
            return True
        return False

    @staticmethod
    def validate_dob(dob) -> bool:
        """
            Function to check dob type and if it meets the requirement of the regex and check if the user is 16 years
            old and above

            @params: dob, the input dob
            @returns: bool, True if valid dob else false
        """
        dob_regex = r"(?:(?:31(/|-|.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(/|-|.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(/|-|.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(/|-|.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"
        if re.match(dob_regex, dob):
            born = datetime.strptime(dob, "%d/%m/%Y").date()
            today = date.today()

            birthday = born.replace(year=today.year)
            if birthday > today:
                if (today.year - born.year - 1) > 16:
                    return True
            else:
                if (today.year - born.year) > 16:
                    return True
        return False

    @staticmethod
    def validate_otp(otp) -> bool:
        """
            Function to check otp type and if it meets the requirement of the regex of only having a 6 numbers

            @params: otp, the input otp
            @returns: bool, True if valid otp else false
        """
        otp_regex = r"[0-9]{6}$"
        if re.match(otp_regex, otp):
            return True
        return False

    @staticmethod
    def validate_salt(salt) -> bool:
        """
            Function to salt password type and if it meets the requirement of the regex with a length of 64 characters
            and contains alphabets and numbers only.

            @params: salt, the input salt
            @returns: bool, True if valid salt else false
        """
        salt_regex = r"[A-Za-z0-9]{64}"
        if re.match(salt_regex, salt):
            return True
        return False

    @staticmethod
    def validate_number(number) -> bool:
        """
            Function to check number type and if it meets the requirement of the regex of number being a int and ranges from
            1 to 10 digits

            @params: number, the input number
            @returns: bool, True if valid number else false
        """
        number_regex = r"[0-9]{1,10}"
        if re.match(number_regex, number):
            return True
        return False

    @staticmethod
    def validate_google_api(captcha_results) -> bool:
        """
            Function that checks the reCaptcha result is valid

            @params:
                captcha_results, the results received
            @returns:
                bool, True if the captcha_results is valid else false
        """
        result_regex = "{'(success)':\s(True|False),\s'(challenge_ts)':\s'\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])T(([0-1][0-9])|(2[0-3])):?[0-5][0-9]:?[0-5][0-9]+Z',\s'hostname':\s'(taurus.sitict.net|127.0.0.1|testkey.google.com)'}"
        if re.match(result_regex, captcha_results):
            return True
        return False

    @staticmethod
    def validate_stock_company_name(companyname) -> bool:
        """
            Function that checks the Stock company name result is valid

            @params:
                companyname, the results received
            @returns:
                bool, True if the companyname is valid else false
        """
        result_regex = "[a-zA-Z0-9 .()&,&;%-]{7,100}"
        if re.match(result_regex, companyname):
            return True
        return False

    @staticmethod
    def validate_stock_logo_url(logo_url) -> bool:
        """
            Function that checks the stock logo url result is valid

            @params:
                logo url, the results received
            @returns:
                bool, True if the logo url is valid else false
        """
        result_regex = "(((?:https:\/\/logo.clearbit.com\/[a-zA-Z0-9()0-]{1,100})\.(?:com|sg|asia|net|listedcompany|wixsite|starland|cc|cn|org|id|education|biz|group|co|edu)(?:\.sg|\.my|\.sg|\.au|\.com|.hk|.tw|.cn|.id)?)|null)"
        if re.match(result_regex, logo_url):
            return True
        return False

    @staticmethod
    def validate_stock_symbol(stock_symbol) -> bool:
        """
            Function that checks the stock logo url result is valid

            @params:
                stock symbol, the results received
            @returns:
                bool, True if the stock symbol is valid else false
        """
        result_regex = "[A-Z0-9]{3,15}.SI"
        if re.match(result_regex, stock_symbol):
            return True
        return False

    @staticmethod
    def validate_stock_sector(sector) -> bool:
        """
            Function that checks the sector result is valid

            @params:
                stock sector, the results received
            @returns:
                bool, True if the stock sector is valid else false
        """
        result_regex = "([A-Za-z\s]{3,45}|null)"
        if re.match(result_regex, sector):
            return True
        return False

    @staticmethod
    def validate_stock_industry(industry) -> bool:
        """
            Function that checks the stock industry result is valid

            @params:
                stock industry, the results received
            @returns:
                bool, True if the stock industry is valid else false
        """
        result_regex = "([A-Za-z &—,-]{3,45}|null)+"
        if re.match(result_regex, industry):
            return True
        return False


class Validation_Functions():
    @staticmethod
    def validate_register(data) -> bool:
        """
            Function that takes in a dictionary and checks if the dictionary values input type are correct

            @params: data, the dictionary input
            @returns: bool, True if the test is valid else false
        """
        if isinstance(data, dict):
            isvalid = True

            if not Validation.validate_text(data['firstName']):
                isvalid = False
            if not Validation.validate_text(data['lastName']):
                isvalid = False
            if not Validation.validate_email(data['email']):
                isvalid = False
            if not Validation.validate_password(data['password']):
                isvalid = False
            if not Validation.validate_password(data['confirm_password']):
                isvalid = False
            if not Validation.validate_dob(data["dob"]):
                isvalid = False

            return isvalid
        return False

    @staticmethod
    def validate_login(email, password) -> bool:
        """
            Function that checks if the email and password input type are correct

            @params:
                email, a string input
                password, a string input of 512 chars
            @returns: bool, True if the test is valid else false
        """
        isvalid = True

        if not Validation.validate_email(email):
            isvalid = False
        if not Validation.validate_password(password):
            isvalid = False

        return isvalid

    @staticmethod
    def validate_new_password(password, salt) -> bool:
        """
            Function that checks if the email and password input type are correct

            @params:
                password, a string input of 512 chars
                salt, a string input of 64 chars
            @returns: bool, True if the test is valid else false
        """
        isvalid = True

        if not Validation.validate_password(password):
            isvalid = False
        if not Validation.validate_salt(salt):
            isvalid = False

        return isvalid

    @staticmethod
    def validate_deposit(amount) -> bool:
        """
            Function that checks if the deposit amount by the teacher is within the range of 1 to 500

            @params:
                amount, a float input of the deposit amount
            @returns: bool, True if the test is valid else false
        """
        if amount > 500 or amount < 1:
            return False
        return True

    @staticmethod
    def validate_profile_update(fn, ln) -> bool:
        """
            Function that checks if the first name and last name type for profile update is valid

            @params:
                fn, the new first name
                ln, the new last name
            @returns: bool, True if the test is valid else false
        """
        isvalid = True

        if not Validation.validate_text(fn):
            isvalid = False
        if not Validation.validate_text(ln):
            isvalid = False

        return isvalid

    @staticmethod
    def validate_purchase_option(quantity, total_price, user_balance) -> tuple[bool, str]:
        """
            Function that checks if the user is valid to make the purchase transaction for the stock

            @params:
                quantity, the total quantity of the stock to purchase
                total_price, the total price of the stock to make payment for
                user_balance, the current balance user is left with
            @returns:
                bool, True if the test is valid else false
                str, message that carries the error if bool is false
        """
        isvalid = True
        msg = ''

        if quantity > 1000000:
            isvalid = False
            msg = "Please enter a valid quantity."
        else:
            if user_balance < total_price:
                isvalid = False
                msg = 'Not enough balance to purchase stock!'
            if quantity < 1:
                isvalid = False
                msg = 'Quantity entered is less than 1!'

        return isvalid, msg

    @staticmethod
    def validate_sell_option(quantity, owned_quantity) -> tuple[bool, str]:
        """
            Function that checks if the user is valid to make the sell transaction for the stock

            @params:
                quantity, the total quantity of the stock to purchase
                owned_quantity, the current quantity of the stock user is holding
            @returns:
                bool, True if the test is valid else false
                str, message that carries the error if bool is false
        """
        isvalid = True
        msg = ''

        if quantity > 1000000:
            isvalid = False
            msg = "Please enter a valid quantity."
        else:
            if quantity < 1:
                isvalid = False
                msg = 'Quantity enter is less than 1!'
            if quantity > owned_quantity:
                isvalid = False
                msg = 'You do not own enough shares of this stock!'

        return isvalid, msg

    @staticmethod
    def validate_yfinance(symbol, ticker) -> bool:
        """
            Function that checks if the ticker values from the yfinance API are valid

            @params:
                symbol, a string input of the stock symbol
                ticker, a dict input of the ticker info
            @returns: bool, True if the test is valid else false
        """

        if not Validation.validate_stock_company_name(ticker.get('longName')):
            return False
        if not Validation.validate_stock_symbol(symbol):
            return False
        if not Validation.validate_stock_logo_url(ticker.get('logo_url')):
            return False
        if not Validation.validate_stock_sector(ticker.get('sector')):
            return False
        return Validation.validate_stock_industry(ticker.get('industry'))