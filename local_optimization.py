import math


Rti = 100  # 5 * 168 =  # Number of potential ride requests
Vti = 442 / 8  # Number of potential available drivers
price_range = 0.25
standard_price = 0.47
max_price = standard_price * (1 + price_range)
max_p_sqrd = math.pow(max_price, 2)


# Cumulative Distribution Function (Fw & Fr)
def F(price):
    return math.pow(price, 2) / math.pow(max_price, 2)


# Demand
def D(r, price):
    return r * (1 - F(price))


def Dinv(r, demand):
    return math.sqrt(max_p_sqrd*(1 - (demand / r)))


# Supply
def S(v, price):
    return v * F(price)


# Revenue
def Rev(r, price):
    platformServiceFee = 0.2
    return D(r, price) * platformServiceFee * price


def T(r, v, p):
    return min(D(r, p), S(v, p))


# TODO: calculate delta T
def revDecrease(r, v, delta_T, optimal_p):
    Tp = T(r, v, optimal_p)
    delta_p = optimal_p - Dinv(r, Tp + delta_T)
    # return Tp * optimal_p - (Tp + delta_T) * (optimal_p - delta_p)
    return Tp * delta_p + delta_T * delta_p - delta_T * optimal_p


# TODO: calculate future V
def revIncrease(r, v, r1, v1):
    pc = calculateClearingPrice(r, v)
    pc1 = calculateClearingPrice(r1, v1)
    return S(v1, pc1) * pc1 - S(v, pc) * pc


def calculateClearingPrice(r, v):
    return math.sqrt((r * max_p_sqrd) / (v + r))


def localOptimization(r, v):
    clearingPrice = calculateClearingPrice(r, v)  # Pc D(p) = S(p)
    maxDemandPrice = math.sqrt(max_p_sqrd / 3)  # Maximizes D(p) * p -> Pd
    print("Pd", maxDemandPrice)
    print("Pc", clearingPrice)

    if maxDemandPrice <= clearingPrice:
        return clearingPrice
    else:
        return maxDemandPrice


def PPricing(r, v, r1):
    """
    Input: Rti, Vti & R(t+1)j
    Output: p*ti, optimal price at time t
    """
    n = 100  # ?
    for i in range(n):
        pti = localOptimization(r, v)
        # Compute RevDec using eq. 9
        revDec = revDecrease()
    for j in range(n):
        v1 = 0  # Calculate using eq. 4
        ptj = localOptimization(r1, v1)
        # Compute RevInc using eq. 14
        revInc = revIncrease()

    # Solve eq. 15 and optimal delta Tt

    # Something else...


if __name__ == "__main__":
    print("The optimal price is", localOptimization(Rti, Vti))
