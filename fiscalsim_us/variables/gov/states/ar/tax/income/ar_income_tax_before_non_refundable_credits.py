from fiscalsim_us.model_api import *


class ar_income_tax_before_non_refundable_credits(Variable):
    "Line 29 of form AR1000F"
    value_type = float
    entity = TaxUnit
    label = "Arkansas income tax before non refundable credits"
    unit = USD
    definition_period = YEAR
    reference = "https://www.dfa.arkansas.gov/images/uploads/incomeTaxOffice/2023_Final_AR1000ES.pdf"
    defined_for = StateCode.AR

    def formula(tax_unit, period, parameters):

        taxable_income = tax_unit("ar_taxable_income", period)
        high_income_threshold = parameters(period).gov.states.ar.tax.income.rates.regular_bracket_max
        litc = tax_unit('ar_income_tax_credit', period)
        high_income_reduction = tax_unit('ar_high_income_reduction', period)

        def round_to_nearest_50(num):
            # Calculate the nearest multiple of 100
            nearest_multiple_of_100 = round(num / 100) * 100
            
            # Get the last two digits
            last_two_digits = num % 100
            
            # Determine the closest ending in "50"
            if last_two_digits <= 50:
                rounded_income = nearest_multiple_of_100 + 50
                return rounded_income
            else:
                rounded_income = nearest_multiple_of_100 - 50
                return rounded_income
            
        rounded_taxable_income = round_to_nearest_50(taxable_income)

        rate = where(taxable_income < high_income_threshold, parameters(period).gov.states.ar.tax.income.rates.rates, parameters(period).gov.states.ar.tax.income.rates.high_income_rates)
        
        tax = rate.calc(rounded_taxable_income) - litc - high_income_reduction



        return tax