from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import Wallet, Transaction


@login_required
def dashboard(request):
    wallet = Wallet.objects.get(user=request.user)

    transactions = Transaction.objects.filter(
        wallet=wallet
    ).order_by('-created_at')[:10]

    return render(
    request,
    'dashboard_mobile.html',
    {
        'wallet': wallet,
        'transactions': transactions
    }
)


@login_required
def deposit(request):
    wallet = Wallet.objects.get(user=request.user)

    if request.method == "POST":
        amount = Decimal(request.POST.get("amount"))

        Transaction.objects.create(
            wallet=wallet,
            transaction_type="Deposit",
            amount=amount
        )

        return redirect("dashboard")

    return render(request, "deposit.html")


@login_required
def withdraw(request):
    wallet = Wallet.objects.get(user=request.user)

    if request.method == "POST":
        amount = Decimal(request.POST.get("amount"))

        if amount <= wallet.balance:

            Transaction.objects.create(
                wallet=wallet,
                transaction_type="Withdraw",
                amount=amount
            )

            return redirect("dashboard")

    return render(request, "withdraw.html")


@login_required
def transfer(request):
    sender = Wallet.objects.get(user=request.user)

    if request.method == "POST":
        account_number = request.POST.get("account_number")
        amount = Decimal(request.POST.get("amount"))

        try:
            receiver = Wallet.objects.get(
                account_number=account_number
            )

            if amount <= sender.balance:

                Transaction.objects.create(
                    wallet=sender,
                    transaction_type="Transfer Sent",
                    amount=amount
                )

                Transaction.objects.create(
                    wallet=receiver,
                    transaction_type="Transfer Received",
                    amount=amount
                )

                return redirect("dashboard")

        except Wallet.DoesNotExist:
            pass

    return render(request, "transfer.html")


@login_required
def transactions(request):
    wallet = Wallet.objects.get(user=request.user)

    transactions = Transaction.objects.filter(
        wallet=wallet
    ).order_by('-created_at')

    return render(
        request,
        "transactions.html",
        {
            "transactions": transactions
        }
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            Wallet.objects.create(
            account_type=form.cleaned_data["account_type"],
    user=user,
    balance=500000,

    first_name=form.cleaned_data["first_name"],
    middle_name=form.cleaned_data["middle_name"],
    last_name=form.cleaned_data["last_name"],

    phone_number=form.cleaned_data["phone_number"],
    address=form.cleaned_data["address"],

    country=form.cleaned_data["country"],
    state=form.cleaned_data["state"],
    city=form.cleaned_data["city"],
    postal_code=form.cleaned_data["postal_code"],

    date_of_birth=form.cleaned_data["date_of_birth"],
)

            login(request, user)

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )

@login_required
def profile(request):
    wallet = Wallet.objects.get(user=request.user)

    return render(
        request,
        "profile.html",
        {
            "wallet": wallet
        }
    )
   
@login_required
def upload_photo(request):
    wallet = Wallet.objects.get(user=request.user)

    if request.method == "POST":
        if "photo" in request.FILES:
            wallet.profile_picture = request.FILES["photo"]
            wallet.save()

            return redirect("profile")

    return render(
        request,
        "upload_photo.html"
    )