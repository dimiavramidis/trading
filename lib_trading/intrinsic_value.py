def main():

    # Calculate and return intrinsic value
    return intrinsic_value_calc(
        operating_cash_flow=7064.00,  # in millions
        total_debt=9602.00,  # in millions
        cash_short_term_investment=13977.00,  # in millions
        cash_flow_growth_rate_short_term=0.1836,  # in percent
        cash_flow_growth_rate_mid_term=0.15,  # in percent
        cash_flow_growth_rate_long_term=0.0418,  # in percent
        number_of_short_term_years=5,
        number_of_mid_term_years=5,
        number_of_long_term_years=10,
        number_of_shares_outstanding=977.0,  # in millions
        beta=1.2  # in percent
    )


# Calculate intrinsic value

1 - (209.00/262.33)


def intrinsic_value_calc(
    operating_cash_flow: float,
    total_debt: float,
    cash_short_term_investment: float,
    cash_flow_growth_rate_short_term: float,
    cash_flow_growth_rate_mid_term: float,
    cash_flow_growth_rate_long_term: float,
    number_of_short_term_years: int,
    number_of_mid_term_years: int,
    number_of_long_term_years: int,
    number_of_shares_outstanding: float,
    beta: float
) -> float:

    # Return discount rate
    discount_rate = discount_rate_calc(
        beta
    )
    print("discount_rate: " + str(discount_rate) + "\n")

    # Get a list of discount rates
    list_discount_rate = create_discount_rate_list(
        discount_rate,
        number_of_short_term_years + number_of_mid_term_years + number_of_long_term_years
    )
    print("list_discount_rate: " + str(list_discount_rate) + "\n")

    # Calculate projected cash flow for short term and long term
    projected_cash_flow = projected_cash_flow_calc(
        operating_cash_flow,
        cash_flow_growth_rate_short_term,
        cash_flow_growth_rate_mid_term,
        cash_flow_growth_rate_long_term,
        number_of_short_term_years,
        number_of_mid_term_years,
        number_of_long_term_years
    )

    print("projected_cash_flow: " + str(projected_cash_flow) + "\n")

    # Get projected_cash_flow discounted
    projected_cash_flow_discounted = projected_cash_flow_discounted_calc(
        projected_cash_flow,
        list_discount_rate
    )
    print("projected_cash_flow_discounted: " +
          str(projected_cash_flow_discounted) + "\n")

    # Determine commulative sum of projected cash flow discounted
    cumulated_projected_cash_flow_discounted = sum(
        projected_cash_flow_discounted)
    print("cumulated_projected_cash_flow_discounted: " +
          str(cumulated_projected_cash_flow_discounted) + "\n")

    # Calculate intrinsic value before cash and debt
    intrinsic_value_before_cash_debt = cumulated_projected_cash_flow_discounted / \
        number_of_shares_outstanding
    print("intrinsic_value_before_cash_debt: " +
          str(intrinsic_value_before_cash_debt) + "\n")

    # Calculate less debt per share
    less_debt_per_share = total_debt / number_of_shares_outstanding
    print("less_debt_per_share: " + str(less_debt_per_share) + "\n")

    # Calculate plus cash per share
    plus_cash_per_share = cash_short_term_investment / number_of_shares_outstanding
    print("plus_cash_per_share: " + str(plus_cash_per_share) + "\n")

    # Determine final intrinsic value
    final_intrinsic_value = intrinsic_value_before_cash_debt + \
        plus_cash_per_share - less_debt_per_share
    print("final_intrinsic_value: " + str(final_intrinsic_value) + "\n")

    # Return final intrinsic value per share
    return final_intrinsic_value

# Determine discount rate


def discount_rate_calc(
    beta: float
) -> float:

    if beta <= 0.80:
        discount_rate = 0.05  # in percent
    elif beta <= 1.0:
        discount_rate = 0.06  # in percent
    elif beta <= 1.1:
        discount_rate = 0.065  # in percent
    elif beta <= 1.2:
        discount_rate = 0.07  # in percent
    elif beta <= 1.3:
        discount_rate = 0.075  # in percent
    elif beta <= 1.4:
        discount_rate = 0.08  # in percent
    elif beta <= 1.5:
        discount_rate = 0.085  # in percent
    elif beta >= 1.5:
        discount_rate = 0.09

    return discount_rate

# Create a list of discount rates


def create_discount_rate_list(
    discount_rate: float,
    number_of_short_and_long_term_years: int,
) -> list:

    # Create and return a list of discount rates
    return [(1-discount_rate) ** i for i in range(1, number_of_short_and_long_term_years+1)]


# Calculate projected cash flow for short term and long term


def projected_cash_flow_calc(
    operating_cash_flow: float,
    cash_flow_growth_rate_short_term: float,
    cash_flow_growth_rate_mid_term: float,
    cash_flow_growth_rate_long_term: float,
    number_of_short_term_years: int,
    number_of_mid_term_years: int,
    number_of_long_term_years: int
) -> list:

    # Calculate projected cash flow for short term
    projected_cash_flow_short_term = cash_flow_growth_rate_short_term_calc(
        operating_cash_flow,
        number_of_short_term_years,
        cash_flow_growth_rate_short_term
    )

    # Calculate projected cash flow for long term
    projected_cash_flow_mid_term = cash_flow_growth_rate_long_term_calc(
        projected_cash_flow_short_term,
        number_of_mid_term_years,
        cash_flow_growth_rate_mid_term
    )

    # Calculate projected cash flow for long term
    projected_cash_flow_long_term = cash_flow_growth_rate_long_term_calc(
        projected_cash_flow_mid_term,
        number_of_long_term_years,
        cash_flow_growth_rate_long_term
    )

    # Return projected cash flow
    return (
        projected_cash_flow_short_term +
        projected_cash_flow_mid_term +
        projected_cash_flow_long_term
    )


# Calculate projected cash flow for short term

def cash_flow_growth_rate_short_term_calc(
    operating_cash_flow: float,
    number_of_short_term_years: int,
    cash_flow_growth_rate_short_term: float
) -> list:
    return [operating_cash_flow*(1+cash_flow_growth_rate_short_term)
            ** i for i in range(1, number_of_short_term_years+1)]


# Calculate projected cash flow for mid term

def cash_flow_growth_rate_long_term_calc(
    list_short_term: list,
    number_of_mid_term_years: int,
    cash_flow_growth_rate_mid_term: float
) -> list:
    return [list_short_term[-1]*(1+cash_flow_growth_rate_mid_term)
            ** i for i in range(1, number_of_mid_term_years+1)]

# Calculate projected cash flow for long term


def cash_flow_growth_rate_long_term_calc(
    list_mid_term: list,
    number_of_long_term_years: int,
    cash_flow_growth_rate_long_term: float
) -> list:
    return [list_mid_term[-1]*(1+cash_flow_growth_rate_long_term)
            ** i for i in range(1, number_of_long_term_years+1)]


def projected_cash_flow_discounted_calc(
    projected_cash_flow: list,
    list_discount_rate: list
) -> list:

    # Return projected cash flow with discount by multiplying each element in list_discount_rate by projected_cash_flow
    return [a*b for a, b in zip(projected_cash_flow, list_discount_rate)]


if __name__ == '__main__':
    main()
