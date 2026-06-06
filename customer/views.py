from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Wallet, Transaction


@login_required
def dashboard(request):
    wallet = Wallet.objects.get(user=request.user)

    transactions = []

    if wallet:
        transactions = Transaction.objects.filter(
            wallet=wallet
        ).order_by('-created_at')[:10]

    return render(
        request,
        'dashboard.html',
        {
            'wallet': wallet,
            'transactions': transactions
        }
    )


def deposit(request):
    wallet = Wallet.objects.get(user=request.user)

    if request.method == "POST":

        amount = Decimal(request.POST.get("amount"))

        wallet.balance += amount
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            transaction_type="Deposit",
            amount=amount
        )

        return redirect("dashboard")

    return render(request, "deposit.html")


@login_required
def withdraw(request):

    if request.method == "POST":

        amount = Decimal(request.POST.get("amount"))

        if amount <= wallet.balance:

            wallet.balance -= amount
            wallet.save()

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

                sender.balance -= amount
                sender.save()

                receiver.balance += amount
                receiver.save()

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

            Wallet.objects.create(user=user)

            login(request, user)

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )