'''
------------------------------------------------------------------------

Fiscal policy functions for unbalanced budgeting. In particular, some
functions require time-path calculation.

------------------------------------------------------------------------
'''

# Packages
import numpy as np
from ogusa import aggregates as aggr

'''
------------------------------------------------------------------------
    Functions
------------------------------------------------------------------------
'''


def D_G_path(r_gov, dg_fixed_values, Gbaseline, p):
    r'''
    Calculate the time paths of debt and government spending

    .. math::
        \begin{split}
        &G_t = g_{g,t}\:\alpha_{g}\: Y_t \\
        &\text{where}\quad g_{g,t} =
          \begin{cases}
            1 \qquad\qquad\qquad\qquad\qquad\qquad\qquad\:\:\:\,\text{if}\quad t < T_{G1} \\
            \frac{\left[\rho_{d}\alpha_{D}Y_{t} + (1-\rho_{d})D_{t}\right] - (1+r_{t})D_{t} - TR_{t} + Rev_{t}}{\alpha_g Y_t} \quad\text{if}\quad T_{G1}\leq t<T_{G2} \\
            \frac{\alpha_{D}Y_{t} - (1+r_{t})D_{t} - TR_{t} + Rev_{t}}{\alpha_g Y_t} \qquad\qquad\quad\:\:\:\,\text{if}\quad t \geq T_{G2}
          \end{cases} \\
        &\quad\text{and}\quad g_{tr,t} = 1 \quad\forall t
      \end{split}

    Args:
        r_gov (Numpy array): interest rate on government debt over the
            time path
        dg_fixed_values (tuple): (Y, total_revenue, TR, D0, G0) values
            of variables that are taken as given in the government
            budget constraint
        Gbaseline (Numpy array): government spending over the time path
            in the baseline equilibrium, used only if
            baseline_spending=True
        p (OG-USA Specifications object): model parameters

    Returns:
        (tuple): fiscal variable path output:

            * D (Numpy array): government debt over the time path
            * G (Numpy array): government spending over the time path
            * D_d (Numpy array): domestic held government debt over the
                time path
            * D_f (Numpy array): foreign held government debt over the
                time path
            * new_borrowing_f: new borrowing from foreigners

    '''
    Y, total_revenue, TR, D0, G0 = dg_fixed_values

    D = np.zeros(p.T + 1)
    growth = (1 + p.g_n) * np.exp(p.g_y)
    D[0] = D0

    if p.baseline_spending:
        G = Gbaseline[:p.T]
    else:
        G = p.alpha_G[:p.T] * Y[:p.T]
        G[0] = G0

    if p.budget_balance:
        G = np.zeros(p.T)
        D_f = np.zeros(p.T)
        D_d = np.zeros(p.T)
    else:
        t = 1
        while t < p.T-1:
            D[t] = ((1 / growth[t]) * ((1 + r_gov[t - 1]) * D[t - 1] +
                                       G[t - 1] + TR[t - 1] -
                                       total_revenue[t - 1]))
            if (t >= p.tG1) and (t < p.tG2):
                G[t] = (growth[t + 1] * (p.rho_G * p.debt_ratio_ss * Y[t] +
                                         (1 - p.rho_G) * D[t]) -
                        (1 + r_gov[t]) * D[t] + total_revenue[t] - TR[t])
            elif t >= p.tG2:
                G[t] = (growth[t + 1] * (p.debt_ratio_ss * Y[t]) -
                        (1 + r_gov[t]) * D[t] + total_revenue[t] - TR[t])
            t += 1

        # in final period, growth rate has stabilized, so we can replace
        # growth[t+1] with growth[t]
        t = p.T - 1
        D[t] = ((1 / growth[t]) * ((1 + r_gov[t - 1]) * D[t - 1] + G[t - 1]
                                   + TR[t - 1] - total_revenue[t - 1]))
        G[t] = (growth[t] * (p.debt_ratio_ss * Y[t]) - (1 + r_gov[t]) * D[t]
                + total_revenue[t] - TR[t])
        D[t + 1] = ((1 / growth[t + 1]) * ((1 + r_gov[t]) * D[t] + G[t] +
                                           TR[t] - total_revenue[t]))
        D_ratio_max = np.amax(D[:p.T] / Y[:p.T])
        print('Maximum debt ratio: ', D_ratio_max)

        # Find foreign and domestic debt holding
        # Fix initial amount of foreign debt holding
        D_f = np.zeros(p.T + 1)
        D_f[0] = p.initial_foreign_debt_ratio * D[0]
        for t in range(0, p.T):
            D_f[t + 1] = ((D_f[t] / growth[t + 1]) +
                          (p.zeta_D[t] * (D[t + 1] -
                                          (D[t] / growth[t + 1]))))
        D_d = D[:p.T] - D_f[:p.T]
        new_borrowing_f = (D_f[1:p.T + 1] * np.exp(p.g_y) *
                           (1 + p.g_n[1:p.T + 1]) - D_f[:p.T])

    return D, G, D_d, D_f[:p.T], new_borrowing_f


def get_D_ss(r_gov, Y, p):
    r'''
    Calculate the steady-state values of government spending and debt

    .. math::
        \begin{split}
            \bar{D} = \alpha_D \bar{Y}\\
            \bar{D} = \alpha_D \bar{Y}\\
        \end{split}

    Args:
        r_gov (scalar): steady-state interest rate on government debt
        Y (scalar): steady-state GDP
        p (OG-USA Specifications object): model parameters

    Returns:
        (tuple): steady-state fiscal variables:

            * D (scalar): steady-state government debt
            * D_d (scalar): steady-state domestic held government debt
            * D_f (scalar): steady-state foreign held government debt
            * new_borrowing: steady-state new borrowing
            * debt_service: steady-state debt service costs
            * new_borrowing_f: steady-state borrowing from foreigners

    '''
    if p.budget_balance:
        D = 0.0
    else:
        D = p.debt_ratio_ss * Y
    debt_service = r_gov * D
    new_borrowing = D * ((1 + p.g_n_ss) * np.exp(p.g_y) - 1)
    # government spends such that it expands its debt at the same rate as GDP
    D_f = p.zeta_D[-1] * D
    D_d = D - D_f
    new_borrowing_f = D_f * (np.exp(p.g_y) * (1 + p.g_n_ss) - 1)

    return D, D_d, D_f, new_borrowing, debt_service, new_borrowing_f


def get_G_ss(Revenue, TR, new_borrowing, debt_service, p):
    r'''
    Calculate the steady-state values of government spending

    .. math::
            \bar{G} = \bar{Rev} + \bar{D}((1 + \bar{g}_n)e^{g_y} - 1) - \bar{TR} - \bar{r}_{gov}\bar{D}

    Args:
        r_gov (scalar): steady-state interest rate on government debt
        Y (scalar): steady-state GDP
        Revenue (scalar): steady-state net tax revenue
        TR (scalar): steady-state transfer spending
        p (OG-USA Specifications object): model parameters

    Returns:
        G (tuple): steady-state government spending

    '''
    if p.budget_balance:
        G = 0.0
    else:
        G = Revenue + new_borrowing - (TR + debt_service)
        print('G components = ', new_borrowing, TR, debt_service)

    return G


def get_r_gov(r, p):
    r'''
    Determine the interest rate on government debt

    .. math::
        r_{gov,t} = \max\{(1-\tau_{d,t}r_{t} - \mu_d, 0.0\}

    Args:
        r (array_like): interest rate on private capital debt over the
            time path or in the steady state
        p (OG-USA Specifications object): model parameters

    Returns:
        r_gov (array_like): interest rate on government debt over the
            time path or in the steady-state

    '''
    r_gov = np.maximum(p.r_gov_scale * r - p.r_gov_shift, 0.00)

    return r_gov
