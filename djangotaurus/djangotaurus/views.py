from .models import *
from .srptools import SRPContext, SRPServerSession
from .srptools.constants import HASH_SHA_256, PRIME_2048, PRIME_2048_GEN

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login as Login, logout as Logout, update_session_auth_hash as update_session
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from timeit import default_timer as timer
from .validation import Validation
import logging

general = settings.LOGGING_GENERAL_FORMAT
dtf = settings.LOGGING_DATETIME_FORMAT
loglevel = settings.LOGGING_LEVEL_FORMAT

# Uncomment for localhost, comment for server
# logfile_local = settings.LOGGING_FILENAME_LOCAL
# logging.basicConfig(format=general, datefmt=dtf, level=loglevel, filename=logfile_local)

# Uncomment for server, comment for localhost
logfile_server = settings.LOGGING_FILENAME_SERVER
logging.basicConfig(format=general, datefmt=dtf, level=loglevel, filename=logfile_server)

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def error(request, error_code=None):
    if error_code:
        error_dict = {
            '400': ['400', "400 Bad Request", "You've sent a bad request"],
            '401': ['401', "401 Unauthorized", "Authorisation Required"],
            '403': ['403', "403 Forbidden", "You shall not pass"],
            '404': ["404", "404 Not Found", "Huh, it seems the page you are looking for does not exist."]
        }
        try:
            current_error = error_dict[error_code]
        except KeyError as ke:
            logger.error(f"Error in accessing page! Error: {str(ke)}")
            return redirect(error, error_code=403)

        return render(request, 'error.html', {'current_error': current_error})
    else:
        return redirect(error, error_code=403)


def staff_check(user):
    return user.is_staff


def get_color(num):
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c',
              '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1',
              '#000075', '#808080']
    color_array = []
    for x in range(num):
        color_array.append(colors[x])

    return color_array


@require_http_methods(["GET"])
def home(request):
    # Grab values instead of ORM objects to significantly reduce load times
    stock_prices = StockPriceCurrent.objects.values('id', 'open', 'close', 'high', 'low',
                                                    'stock__company_name', 'stock__stock_symbol', 'stock__company_desc',
                                                    'stock__sector',
                                                    'stock__industry', 'stock__image_url', 'stock__id')

    return render(request, 'index.html', {'stock_prices': stock_prices})


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def portfolio(request, user_id=None):
    try:
        if user_id and request.user.is_staff:
            user = User.objects.get(id=user_id)
        else:
            user = request.user
        portfolio_data = []
        transactions = Transaction.objects.get_active_transactions(user, active=True)
        for transaction in transactions:
            if transaction.lot_quantity > 0:
                invested_amount = round(float(transaction.price) * transaction.lot_quantity, 3)
                current_value = StockPriceCurrent.objects.get_current_price(transaction.stock)
                portfolio_data.append(
                    {'symbol': transaction.stock.stock_symbol, 'company': transaction.stock.company_name,
                     'option': transaction.option, 'invested': invested_amount, 'price': current_value,
                     'id': transaction.stock.id, 'quantity': transaction.lot_quantity})
        return render(request, 'portfolio.html', {'portfolio': portfolio_data})
    except Exception as e:
        messages.error(request, "Something went wrong, please try again.")
        logger.error(f"Session is corrupted, user object retrieved is manipulated! Error: {str(e)}")
        redirect(logout)


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def history(request, user_id=None):
    try:
        if user_id and request.user.is_staff:
            user = User.objects.get(id=user_id)
        else:
            user = request.user
        history_data = []
        transactions = Transaction.objects.get_active_transactions(user, active=False)
        for transaction in transactions:
            original_transaction = Transaction.objects.get_active_transactions(user, True, transaction.stock,
                                                                               transaction.option)
            difference = original_transaction.first().price - transaction.price
            profit = difference if transaction.option == 'SELL' else -difference
            profit *= transaction.lot_quantity
            history_data.append(
                {'option': transaction.option, 'symbol': transaction.stock.stock_symbol, 'profit': profit,
                 'purchase': original_transaction.first().price, 'return': transaction.price,
                 'id': transaction.stock.id,
                 'quantity': transaction.lot_quantity})

        return render(request, 'history.html', {'history_list': history_data})
    except Exception as e:
        messages.error(request, "Something went wrong, please try again.")
        logger.error(f"Session is corrupted, user object retrieved is manipulated! Error: {str(e)}")
        redirect(logout)


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def favourites(request):
    try:
        fav_data = []
        favourite = Favourites.objects.get_favourites(request.user)
        for fav in favourite:
            current_value = StockPriceCurrent.objects.get_current_price(fav.stock)
            fav_data.append(
                {'symbol': fav.stock.stock_symbol, 'company': fav.stock.company_name, 'sector': fav.stock.sector,
                 'industry': fav.stock.industry, 'value': current_value, 'id': fav.stock.id})
        return render(request, 'favourites.html', {'favourites': fav_data})
    except Exception as e:
        messages.error(request, "Something went wrong, please try again.")
        logger.error(f"Session is corrupted, user object retrieved is manipulated! Error: {str(e)}")
        redirect(logout)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    elif request.session.get('otp_verified'):
        del request.session['otp_verified']
        try:
            user = User.objects.get(email=request.session.get('email'))
        except Exception as e:
            messages.error(request, "Something went wrong, please try again.")
            logger.error(f"Something went wrong! Please try again! Error: {str(e)}")
            return redirect(home)
        user.remove_all_sessions()
        messages.success(request,
                         "Welcome, " + str(user.profile.first_name) + " " + str(user.profile.last_name) + "!")
        Login(request, user)
        user.reset_login_attempts()
        return redirect(home)
    else:
        if request.method == 'POST':
            captcha_response = str(request.POST.get('captcha2'))
            if request.POST['state'] and request.POST['email']:
                state = str(request.POST['state'])
                email = str(request.POST['email'])
                if not Validation.validate_email(email):
                    messages.error(request, "Invalid credentials entered")
                    return JsonResponse({"page": "/login/"})
            else:
                messages.error(request, "Please try again.")
                return JsonResponse({"page": "/login/"})

            if state == '1':
                if Authentication.is_human(captcha_response):
                    try:
                        user = User.objects.get(email=email)
                        # Check if account is locked
                        if user.account_lock:
                            last_attempt = user.last_login_attempt
                            elapsed = (datetime.now(timezone.utc) - last_attempt).total_seconds()
                            if elapsed >= 900:
                                user.lock_account(False)
                                user.reset_login_attempts()
                            else:
                                messages.error(request, "Account has been locked. Please try again in 15 minutes.")
                                return JsonResponse({"page": "/login/"})

                        # Create srp object
                        srp_test = SRPContext(email, prime=PRIME_2048, generator=PRIME_2048_GEN, bits_random=2048,
                                              hash_func=HASH_SHA_256, bits_salt=256)

                        pass_verifier, salt = Authentication.retrieveVerifierSalt(email)
                        srp_session = SRPServerSession(srp_test, pass_verifier)
                        # Create server public key
                        server_public = srp_session.public

                        # Current user paired with server session
                        request.session["srp_session"] = srp_session

                        # Salt and server pub return to client to compute
                        salt_BB = {
                            "salt": salt,
                            "server_pub": server_public
                        }
                        return JsonResponse(salt_BB)

                    except ObjectDoesNotExist:
                        messages.error(request, "Incorrect credentials entered")
                        logger.error(f"Incorrect credentials entered for the following email: {email}")
                        return JsonResponse({'page': '/login/'})
                    except Exception as e:
                        messages.error(request, "Something went wrong, please try again.")
                        logger.error(f"Something went wrong, please try again! Error: {str(e)}")
                        return JsonResponse({'page': '/login/'})
                else:
                    messages.error(request, "Please tick ReCAPTCHA widget to proceed.")
                    logger.error(f"Did not pass the captcha!")
                    return JsonResponse({'page': '/login/'})

            # State 2 - Client send M1, email, client pub key
            elif state == '2':
                try:
                    m1 = str(request.POST['M1'])
                    client_public = str(request.POST['client_pub'])
                    srp_session = request.session["srp_session"]
                    pass_verifier, salt = Authentication.retrieveVerifierSalt(email)

                    # Server process client pub and salt
                    srp_session.process(client_public, salt)
                    result = srp_session.verify_proof(m1)

                    if result:
                        # If match, compute M2 and store M1 and M2 data into dict
                        server_session_key_proof_hash = srp_session.key_proof_hash
                        m2 = {"server_session_key_proof_hash": server_session_key_proof_hash.decode('utf-8')}

                        return JsonResponse({"m2": m2})

                    else:
                        logger.error(f"Incorrect credentials entered for the following email: {email}")
                        messages.error(request, "Incorrect credentials entered")
                        user = User.objects.get(email=email)

                        # Login fail, add to login attempt count or account lock if this is the fifth try
                        if user.login_attempts < 5:
                            user.set_login_attempt()
                        else:
                            user.lock_account()
                            messages.error(request, "Maximum number of login attempts reached.")
                        return JsonResponse({"page": "/login/"})

                except Exception as e:
                    logger.error(f"Something went wrong, please try again! Error: {e}")
                    messages.error(request, "Something went wrong, please try again.")
                    return JsonResponse({'page': '/login/'})

            # State 3 will sent when client confirm server session key
            elif state == "3":
                try:
                    # Pop the item from session and make a final check
                    request.session.pop('srp_session')
                    request.session['email'] = email
                    user = User.objects.get(email=email)

                    if user.verified:
                        AccessToken.objects.generate_token(user, 'OTP', 3)
                        messages.success(request, "An OTP has been sent to your email!")
                        return JsonResponse({"page": "/otp/login"})
                    else:
                        return JsonResponse({"page": "/verifyEmail/"})
                except Exception as e:
                    messages.error(request, "Something went wrong, please try again.")
                    logger.error(f"Something went wrong, please try again! Error: {str(e)}")
                    return JsonResponse({'page': '/login/'})
            else:
                messages.error(request, "Something went wrong, please try again.")
        sitekey = settings.GOOGL_RECAPTCHA_SITE_KEY
        return render(request, 'login.html', {'sitekey': sitekey})


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def logout(request):
    Logout(request)
    return redirect(login)


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        messages.warning(request, "Invalid access to website page")
        return redirect(home)
    else:
        sitekey = settings.GOOGL_RECAPTCHA_SITE_KEY
        try:
            if request.method == 'POST':
                captcha_response = str(request.POST['captcha'])

                if Authentication.is_human(captcha_response):
                    user = Authentication.register(dict(request.POST.items()))
                    request.session['email'] = user.email
                    AccessToken.objects.generate_token(user, 'VERIFY', 1440)
                    return JsonResponse({'page': '/verifyEmail/'})
                else:
                    messages.error(request, "Please tick ReCAPTCHA widget to proceed.")
                    logger.error("Not human! Please tick ReCAPTCHA widget to proceed!")
                    return JsonResponse({'page': '/register/'})
        except Exception as e:
            messages.error(request, "Something went wrong, please try again.")
            logger.error(f"Something went wrong, please try again! Error: {str(e)}")
            
    return render(request, 'register.html', {'sitekey': sitekey})


@require_http_methods(["GET", "POST"])
def otp(request, next):
    wait = 60
    header = request.META.get('HTTP_REFERER')
    split_str = header.split('/') if header else ''
    referer = split_str[-2] if len(split_str) > 1 else ''
    if referer in settings.ALLOWED_REFERERS:
        try:
            email = str(request.session.get('email'))
            if request.method == 'POST':
                user = User.objects.get(email=email)
                if request.POST.get('btnResend') is None:
                    otp = str(request.POST.get('otp1') + request.POST.get('otp2') + request.POST.get(
                        'otp3') + request.POST.get('otp4') + request.POST.get('otp5') + request.POST.get('otp6'))
                    # Perform validation check. Ensure it is only 6 digits
                    if Validation.validate_otp(otp):
                        try:
                            AccessToken.objects.verify_token(otp)
                            AccessToken.objects.expire_token(otp)

                            if next == "login":
                                request.session['otp_verified'] = True
                            elif next == "logout":
                                request.user.delete_user()
                                messages.success(request, "Thank you for learning from us. Goodbye!")
                            elif next == "profile":
                                messages.success(request, "Password was changed successfully!")
                            return redirect(next)
                        except Exception as e:
                            messages.error(request, f"{e} Try requesting for a new OTP")
                            logger.error(f"Try requesting for a new OTP! Error: {str(e)}")
                    else:
                        messages.error(request, "OTP does not match.")
                # Resend OTP
                else:
                    if timer() - request.session.get('otp_time') < wait:
                        remaining = wait - (round(timer() - request.session.get('otp_time')))
                        messages.error(request, f"Please wait for {remaining} seconds before resending OTP.")
                    else:
                        AccessToken.objects.expire_old_token(user, "OTP")
                        AccessToken.objects.generate_token(user, 'OTP', 3)
                        request.session['otp_time'] = timer()
                        messages.success(request, "A new OTP has been sent to your email!")
            elif request.method == 'GET':
                request.session['otp_time'] = timer()
            return render(request, 'otp.html', {'email': email})

        except Exception as e:
            messages.error(request, 'Something went wrong, please try logging in again.')
            logger.error(f"Something went wrong, please try logging in again! Error: {str(e)}")
            return redirect(error, error_code=400)
    else:
        messages.error(request, 'Unauthorized access to page.')
        return redirect(error, error_code=403)


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def profile(request):
    try:
        if request.method == 'POST':
            delete_user = request.POST.get('delete', False)
            if delete_user:
                AccessToken.objects.generate_token(request.user, 'OTP', 3)
                request.session['email'] = request.user.email
                messages.success(request, "A new OTP has been sent to your email!")
                return redirect(otp, next='logout')
            else:
                fn = str(request.POST['fn'])
                ln = str(request.POST['ln'])

                if request.user.profile.update_profile(fn, ln):
                    messages.success(request, "Profile updated successfully")
                else:
                    messages.success(request, "Profile was not updated successfully")

        industry_invested = User.get_invested_industry(request.user)
        color_array = get_color(len(industry_invested))

        return render(request, 'profile.html', {'dob': request.user.profile.date_of_birth.strftime('%d/%m/%Y'),
                                                'investedIndustry': industry_invested, 'colorArray': color_array,
                                                'chartTitle': "Total Invested",
                                                'invested': request.user.get_invested_amount(),
                                                'total': request.user.get_total_amount()})
    except Exception as e:
        messages.error(request, "Something went wrong, please try again.")
        logger.error(f"Something went wrong, please try again! Error: {str(e)}")
        redirect(logout)


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def changePassword(request):
    try:
        # Check if current password in DB matches user entered password
        if request.method == 'POST':
            state = str(request.POST['state'])
            if state == '1':
                return JsonResponse({'email': request.user.email, 'salt': request.user.salt})
            elif state == '2':
                if request.user.password == request.POST['old_password']:
                    new_pw = str(request.POST['new_password'])
                    cfm_pw = str(request.POST['confirm_password'])
                    salt = str(request.POST['salt'])

                    # Check if user entered new password and confirm password matches
                    if new_pw == cfm_pw:
                        request.user.set_password(new_pw, salt)
                        user = request.user
                        user.save()
                        update_session(request, user)
                        AccessToken.objects.generate_token(user, 'OTP', 3)
                        messages.success(request, "An OTP has been sent to your email!")
                        return JsonResponse({'page': '/otp/profile'})
                    else:
                        messages.error(request, "New password and Confirm password do not match")
                        return JsonResponse({'page': '/changePassword/'})
                else:
                    messages.error(request, "Old password and Current password do not match")
                    return JsonResponse({'page': '/changePassword/'})
        return render(request, 'changePassword.html')
    except Exception as e:
        messages.error(request, "Something went wrong, please try again.")
        logger.error(f"Something went wrong, please try again! Error: {str(e)}")
        return redirect(changePassword)


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
@user_passes_test(staff_check, login_url=home)
def users(request):
    students = User.objects.filter(is_staff='False')
    return render(request, 'users.html', {'students': students})


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
@user_passes_test(staff_check, login_url=home)
def staffUserProfile(request, user_id):
    student = User.objects.get(id=user_id)
    if request.method == 'POST':
        reset_user = request.POST.get('reset', False)

        if reset_user:
            student.profile.reset_profile()
            messages.success(request, student.profile.first_name + " " + student.profile.last_name +
                             "'s profile have been reset successfully")
        else:
            amount = request.POST['deposit']
            if student.profile.modify_balance(amount) is True:
                messages.success(request, "SGD " + amount + " have been added successfully")
            else:
                messages.error(request, "SGD " + amount + " does not fall within the limits of $0 - $500.")

    industry_invested = User.get_invested_industry(student)
    color_array = get_color(len(industry_invested))
    return render(request, 'staffUserProfile.html', {'student': student, 'invested': student.get_invested_amount(),
                                                     'total': student.get_total_amount(),
                                                     'investedIndustry': industry_invested,
                                                     'colorArray': color_array, 'chartTitle': "Total Invested"})


@require_http_methods(["GET", "POST"])
def forgotPassword(request):
    if request.user.is_authenticated:
        return redirect(error, error_code=403)
    else:
        try:
            if request.method == 'POST':
                email = str(request.POST.get('email'))
                if Validation.validate_email(email):
                    user = User.objects.get(email=email)
                    AccessToken.objects.expire_old_token(user, 'RESETPW')
                    AccessToken.objects.generate_token(user, 'RESETPW', 5)
                    messages.success(request, "A password reset link will be sent to your email if it is valid!")
                else:
                    messages.error(request, "Please enter a valid email address format.")
            return render(request, 'forgotPassword.html')

        except ObjectDoesNotExist:
            logger.error(f"Email does not exist!")
            messages.success(request, "A password reset link will be sent to your email if it is valid!")
        except Exception as e:
            messages.error(request, f"{e} Please request for a new link.")
            logger.error(f"Please request for a new link. Error {str(e)}")
        return redirect(login)


@require_http_methods(["GET", "POST"])
def resetPassword(request, access_token):
    if request.user.is_authenticated:
        return redirect(error, error_code=403)
    else:
        try:
            if request.method == 'POST':
                user = AccessToken.objects.verify_token(access_token)
                state = str(request.POST['state'])
                if state == '1':
                    email = user.email
                    return JsonResponse({'email': email})
                elif state == '2':
                    new_password = str(request.POST['password'])
                    cfm_password = str(request.POST['confirm_password'])
                    salt = str(request.POST['salt'])
                    if new_password == cfm_password:
                        user.set_password(new_password, salt)
                        messages.success(request, "Password updated successfully")
                        AccessToken.objects.expire_token(access_token)
                        return JsonResponse({'page': '/login/'})
                    else:
                        messages.error(request, "New password and Confirm password do not match")

            return render(request, 'resetPassword.html', {"access_token": access_token})
        except Exception as e:
            messages.error(request, f'{e} Try requesting for a new link.')
            logger.error(f"Please request for a new link. Error {str(e)}")
            return redirect(home)


@require_http_methods(["POST", "GET"])
def verifyEmail(request):
    if request.user.is_authenticated:
        return redirect(error, error_code=403)
    else:
        wait = 60
        if request.method == 'POST':
            if request.POST.get('resend', False):
                user = User.objects.get(email=request.session.get('email'))

                if timer() - request.session.get('verify_time') < wait:
                    remaining = wait - (round(timer() - request.session.get('verify_time')))
                    messages.error(request, f"Please wait for {remaining} seconds before resending link.")
                else:
                    AccessToken.objects.expire_old_token(user, 'VERIFY')
                    AccessToken.objects.generate_token(user, 'VERIFY', 1440)
                    request.session['verify_time'] = timer()
                    messages.success(request, "A new verification link has been sent to your email!")
        elif request.method == 'GET':
            request.session['verify_time'] = timer()

        return render(request, 'verifyEmail.html', {'email': request.session.get('email')})


@require_http_methods(["GET", "POST"])
def verifyCheck(request, access_token):
    try:
        user = AccessToken.objects.verify_token(access_token)
        user.set_verified()
        AccessToken.objects.expire_token(access_token)
        messages.success(request, 'Congratulations! Your email has been verified!')
        return redirect(login)
    except Exception as e:
        messages.error(request, f'{e} Try resending the verification email.')
        logger.error(f"Try resending the verification email. Error {str(e)}")
        return redirect(verifyEmail)


@require_http_methods(["GET", "POST"])
# @TODO validation
def stockDetails(request, stock_id):
    stock = Stock.objects.get(id=stock_id)

    if request.method == 'POST':
        if request.POST.get('option') == 'fav':
            Favourites.objects.set_favourite(request.user, stock)
            messages.success(request, 'Stock successfully saved to favourites.')
        elif request.POST.get('option') == 'unfav':
            Favourites.objects.set_favourite(request.user, stock, False)
            messages.success(request, 'Stock successfully removed from favourites.')

    stock_price = StockPriceCurrent.objects.get(stock=stock)

    buy_options = Transaction.objects.get_active_transactions(request.user, option='BUY', stock=stock)
    if buy_options: buy_options = buy_options.first()

    sell_options = Transaction.objects.get_active_transactions(request.user, option='SELL', stock=stock)
    if sell_options: sell_options = sell_options.first()

    favourite = Favourites.objects.is_favourite(request.user, stock)

    chart_date = ["Date"]
    chart_data = ["Price"]

    ticker = yf.Ticker(stock.stock_symbol).history()
    for i in range(len(ticker.index)):
        chart_date.append(ticker.index[i].strftime("%d/%m/%Y"))
        chart_data.append({'open': round(ticker.get('Open')[i], 3), 'high': round(ticker.get('High')[i], 3),
                           'low': round(ticker.get('Low')[i], 3), 'close': round(ticker.get('Close')[i], 3)})

    return render(request, 'stockDetails.html',
                  {'stock': stock, 'price': stock_price, 'fav': favourite, 'buy': buy_options,
                   'sell': sell_options, 'chart_date': chart_date, 'chart_data': chart_data})


@require_http_methods(["GET", "POST"])
def buyStock(request):
    if request.method == 'POST':
        try:
            stock = Stock.objects.get(id=str(request.POST.get('stock_id')))
            Transaction.objects.purchase_option(request.user, stock, str(request.POST.get('option')),
                                                int(request.POST.get('quantity')))
            messages.success(request, 'Stock successfully purchased.')
        except (TypeError, ValueError):
            messages.error(request, "Please enter a valid quantity.")
            logger.error(f"Please enter a valid quantity. Error: {str(TypeError), str(ValueError)}")
        except Exception as e:
            messages.error(request, e)
            logger.error(f"Please enter a valid quantity. Error: {str(e)}")
        return redirect(stockDetails, stock_id=request.POST.get('stock_id'))
    else:
        messages.warning(request, "Invalid access to website page")
        return redirect(error, error_code=403)


@require_http_methods(["GET", "POST"])
def sellStock(request):
    if request.method == 'POST':
        try:
            stock = Stock.objects.get(id=str(request.POST.get('stock_id')))
            if request.POST.get('buyOpt'):
                Transaction.objects.sell_option(request.user, stock, str(request.POST.get('option')),
                                                int(request.POST.get('buyOpt')))
                messages.success(request, 'Stock successfully sold.')
            elif request.POST.get('sellOpt'):
                Transaction.objects.sell_option(request.user, stock, str(request.POST.get('option')),
                                                int(request.POST.get('sellOpt')))
                messages.success(request, 'Stock successfully sold.')
            else:
                messages.error(request, "Please enter a valid quantity.")
        except (TypeError, ValueError):
            messages.error(request, "Please enter a valid quantity.")
            logger.error(f"Please enter a valid quantity. Error: {str(TypeError), str(ValueError)}")
        except Exception as e:
            messages.error(request, e)
            logger.error(f"Please enter a valid quantity. Error: {str(e)}")
        return redirect(stockDetails, stock_id=request.POST.get('stock_id'))
    else:
        messages.warning(request, "Invalid access to website page")
        return redirect(error, error_code=403)
