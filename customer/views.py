from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Wallet, Transaction


def dashboard(request):
    wallet = Wallet.objects.first()

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
    wallet = Wallet.objects.first()

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


def withdraw(request):
    wallet = Wallet.objects.first()

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


def transfer(request):
    sender = Wallet.objects.first()

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


def transactions(request):
    wallet = Wallet.objects.first()

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