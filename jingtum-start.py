import time

from jingtumsdk.account import FinGate, Wallet
from jingtumsdk.operation import PaymentOperation, OrderOperation, CancelOrderOperation

fingate = FinGate()
fingate.setTest(True)
fingate_address = "jpLpucnjfX7ksggzc9Qw6hMSm1ATKJe3AF"
fingate_secret = "sha4eGoQujTi9SsRSxGN5PamV3YQ4"

coinsCode = "00000005"
coinsSecret = "b33802b7f345fc44e6bd1d3b11c86b412de9ec38"

coins_issuer = "jBciDE8Q3uJjf111VeiUNM775AMKHEbBLS"

coins = "8200000005000020170006000000000020000001"
coins_address = "jG4oHTKopzG1JXjCRd23HdXvXBAAvCSSjr"
coins_secret = "sn5bGPAExY7H4xaDn2PJzoUbzpcbz"

test_address = "jank2wRC3MVaiH6zQwJNJx4qs7TnvjMz3K"
test_address_scret = "sh21U4jFGKxrMw3vGhMdtWzB7ajwA"


def test_create_wallet():
    ret = fingate.createWallet()
    if ret.has_key("success") and ret["success"]:
        my_address, my_secret = ret["wallet"]["address"], ret["wallet"]["secret"]
        print("My Account: %s-%s" % (my_address, my_secret))
        return ret
    return None


def test_acitivte_wallet():
    ret = fingate.createWallet()
    if ret.has_key("success") and ret["success"]:
        my_address, my_secret = ret["wallet"]["address"], ret["wallet"]["secret"]
        print("My Account: %s-%s" % (my_address, my_secret))
        result = fingate.activeWallet(fingate_address, fingate_secret, my_address,
                                      is_sync=True)
        print result


def test_wallet_balance():
    # wallet = Wallet(fingate_address, fingate_secret)
    wallet = Wallet(test_address, test_address_scret)
    ret = wallet.getBalance()
    balances = ret['balances']
    for balance in balances:
        print balance


def test_payment():
    submitOperation = PaymentOperation(coins_address)
    submitOperation.addAmount(coins, 1, coins_address)
    submitOperation.addDestAddress(test_address)
    submitOperation.addSrcSecret(coins_secret)
    subRet = submitOperation.submit()
    print  subRet
    wallet = Wallet(test_address, test_address_scret)
    ret = wallet.getBalance()
    balances = ret['balances']
    for balance in balances:
        print balance


def test_payment_list():
    wallet = Wallet(coins_address, coins_secret)
    paymentListRet = wallet.getPaymentList()
    paymentList = paymentListRet['payments']
    for payment in paymentList:
        print  payment


def test_order():
    wallet = Wallet(coins_address, coins_secret)
    ret = wallet.getBalance()
    balances = ret['balances']
    for balance in balances:
        print balance

    orderOperation = OrderOperation(coins_address)
    orderOperation.addSrcSecret(coins_secret)
    orderOperation.setOrderType(False)
    orderOperation.setTakeGets(coins, 1, coins_issuer)
    orderOperation.setTakePays("SWT", 0.1)
    ret = orderOperation.submit()
    print ret

    odo = OrderOperation(test_address)
    odo.addSrcSecret(test_address_scret)
    odo.setOrderType(False)
    odo.setTakeGets("SWT", 0.1)
    odo.setTakePays(coins, 1, coins_issuer)
    odoRet = odo.submit()
    print odoRet
    time.sleep(30)

    ret = wallet.getOrder(ret['hash'])
    print ret
    ret = wallet.getOrder(odoRet['hash'])
    print ret

    orderList = wallet.getOrderList()
    print orderList


def test_cancel_order_and_transaction():
    orderOperation = OrderOperation(coins_address)
    orderOperation.addSrcSecret(coins_secret)
    orderOperation.setOrderType(False)
    orderOperation.setTakeGets(coins, 1, coins_issuer)
    orderOperation.setTakePays("SWT", 0.1)
    ret = orderOperation.submit()
    print ret

    sequence = ret['sequence']
    cancelOrderOperation = CancelOrderOperation(coins_address)
    cancelOrderOperation.addSrcSecret(coins_secret)
    cancelOrderOperation.setOrderNum(sequence)
    cancelRet = cancelOrderOperation.submit()
    print cancelRet

    wallet = Wallet(coins_address, coins_secret)
    ret = wallet.getOrder(ret['hash'])
    print ret
    ret = wallet.getTransaction(ret['hash'])
    print ret
    transaction = ret['transaction']
    type = transaction['type']
    print type


def test_transactions():
    wallet = Wallet(coins_address, coins_secret)
    ret = wallet.getTransactionList()
    print ret
    payments = ret['payments']
    for payment in payments:
        print payment


def test_issue_custom_query_issue():
    coinsFingate = FinGate()
    coinsFingate.setTest(True)
    coinsFingate.setConfig(coinsCode, coinsSecret)
    ret = coinsFingate.issueCustomTum(coinsFingate.getNextUUID(), coins, "123.45", test_address)
    print ret

    ret = coinsFingate.queryIssue(ret['order'])
    print ret

    wallet = Wallet(test_address, test_address_scret)
    ret = wallet.getBalance()
    balances = ret['balances']
    for balance in balances:
        print balance


def test_query_custom():
    coinsFingate = FinGate()
    coinsFingate.setTest(True)
    coinsFingate.setConfig(coinsCode, coinsSecret)
    ret = coinsFingate.queryCustomTum(coins, time.time())
    print ret


if __name__ == '__main__':
    # test_create_wallet()
    # test_acitivte_wallet()
    # test_wallet_balance()
    # test_payment()
    # test_payment_list()
    # test_order()
    # test_cancel_order_and_transaction()
    # test_transactions()
    test_issue_custom_query_issue()
    # test_query_custom()
