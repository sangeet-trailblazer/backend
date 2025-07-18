this is backend readme file
technologies used:PYTHON DJANGO with REST FRAMEWORKS

features:
1. OTP System for USERS if incase they forget password
2. login for 2 types of users doctor and
3. Changing password
4. OTP auto delete from the database verified and unverified if user completes one verification step

development done using:
1. python 3.12v
2. DJANGO
3. twilio
4. database store using Postgre sql


starting the backend:
step1: cd ai_backend
step2: cd..
step3: ..\env\Scripts\activate
step4: python manage.py runserver

twilio authentication credentials:
this is located under the main app name i.e data's views.py
make sure to register the phone number before using the OTP feature in the website

main API endpoints:

  Endpoint	          Method	     Description
/api/register/ 	       POST	     Register a new user
/api/login/	           POST	     Log in with username and password
/api/logout/	         POST	     Log out and blacklist refresh token
/api/password_change/  POST	    Change password (authenticated)
/auth/send-otp/	       POST	    Forgot password - Send/Verify OTP & Reset
etc...

Forgot password (inside views.py inside data)
steps:
1. send OTP 
  def generate_otp():
    return str(random.randint(1000, 9999))
    if step == "send_otp":# step1
        raw_phone = request.data.get('phone', '')
        request_phone = '+91' + raw_phone[-10:]
        print(f"Username: {username}, Phone: {request_phone}")

        try:
            user = User.objects.get(username=username)
            db_phone = user.phonenumber
            normalized_db_phone = '+91' + db_phone[-10:]

            if request_phone != normalized_db_phone:
                return Response({"error": "Username and phone number do not match."}, status=400)

            otp = generate_otp()
            print(f"Generated OTP for {username}: {otp}")#using the random functon inside the generate OTP function

            # Save OTP to otpstore database
            OTPStore.objects.create(
                username=username,
                otp=otp,
                verified=False,
                timestamp=timezone.now()# latest password to be checked for the user
            )

            #sending OTP via Twilio
            try:
                client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f"Your OTP is {otp}",
                    from_=TWILIO_PHONE_NUMBER,
                    to=request_phone
                )
                print(f"OTP sent. Twilio SID: {message.sid}")
            except Exception as e:
                print("Twilio error:", e)
                return Response({"error": f"Failed to send SMS: {str(e)}"}, status=500)

            return Response({"message": "OTP sent"})

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

2. verify OTP
  elif step == "verify_otp": #step 2
        otp = request.data.get('otp', '').strip()# for any blank spaces we use 
        expiration_time = timezone.now() - timedelta(minutes=5)

        try:
            # Delete expired OTPs
            OTPStore.objects.filter(username=username, timestamp__lt=expiration_time).delete()

            # Get most recent valid OTP
            record = OTPStore.objects.filter(
                username=username,
                timestamp__gte=expiration_time
            ).order_by('-timestamp').first()

            if not record:
                return Response({"error": "OTP not found or expired"}, status=404)

            if record.otp == otp:
                record.verified = True
                record.save()
                return Response({"message": "OTP verified"})
            else:
                return Response({"error": "Incorrect OTP"}, status=400)

        except Exception as e:
            print("OTP verify error:", e)
            return Response({"error": "Something went wrong while verifying OTP"}, status=500)
3. reset password and then deletion of the verified and unverified otp
    elif step == "reset_password":
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        try:
            record = OTPStore.objects.filter(username=username).order_by('-timestamp').first()
            if not record or not record.verified:
                return Response({"error": "OTP not verified"}, status=400)

            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            # Delete all OTPs for this user after one gets verified.
            OTPStore.objects.filter(username=username).delete()

            return Response({"message": "Password reset successful"})

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    return Response({"error": "Invalid step"}, status=400)
            
    OTPStore.objects.filter(username=username).delete() (insideviews.py)


Change password ( inside views.py data)
steps:
1. ask for old password and verify new and confirm password
  if not user.check_password(old_password):# verification whether the old password is correct or not
        return Response(
            {"error": "Old password is incorrect."},
            status=status.HTTP_400_BAD_REQUEST #for wrong password
        )
  if new_password != confirm_password:
        return Response(
            {"error": "New password and confirm password do not match."},
            status=status.HTTP_400_BAD_REQUEST
        )
2. if  everything okay Successfully password will be set
full code :
  #function for password_change
@api_view(['POST']) #method =POST because we are changing it
@authentication_classes([JWTAuthentication]) #uses Jwt
@permission_classes([IsAuthenticated])#only for selected users
def password_change(request):#function
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    # for any empty space
    if not all([old_password, new_password, confirm_password]):
        return Response(
            {"error": "All fields are required."},#if left empty
            status=status.HTTP_400_BAD_REQUEST #400= error
        )

    #Check if old password matches
    if not user.check_password(old_password):# verification whether the old password is correct or not
        return Response(
            {"error": "Old password is incorrect."},
            status=status.HTTP_400_BAD_REQUEST #for wrong password
        )

    # checking if both the passwords matched or not new & confirm
    if new_password != confirm_password:
        return Response(
            {"error": "New password and confirm password do not match."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update password and saving it
    user.set_password(new_password)
    user.save()



Login(inside views.py) 
1. User requires username and password for login
2. which is Provided by the hospital

Features after Login for a Doctor
1.  Add New patients
  details: CrNo', 'Name', 'Age', 'Gender', 'Occupation', 'ConsultingDoctor', 'Diagnosis', 'FirstVisit', 'followups' '''defined inside  serializers.py'''
2. Add old cases
details needed: CR number
3. Patients under you
  filter: search by Name

Features of ADMIN
1. Can create user of two types Doctor or Admin
  Credentails to be added and set: Full name, Role,Doctor,Username,FirstName,SetPassword
2.  Add a new Case (as same as in the case of a doctor)
3.  add old cases

database details:
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ai_db',
        'USER':'postgres',
        'PASSWORD':'mAchchh@r123',
        'HOST': 'localhost',
        'PORT':'5432',
    }
}
Paths this is under Urls.py
  this is used for routing
      path('password_change/', views.password_change, name='password_change'),
      path('forget_password/', forget_password, name='forget_password'),
      path('send-otp/', forget_password),
      path('send-otp/', forget_password),
      path('verify-otp/', forget_password),
      path('reset-password/', forget_password),




