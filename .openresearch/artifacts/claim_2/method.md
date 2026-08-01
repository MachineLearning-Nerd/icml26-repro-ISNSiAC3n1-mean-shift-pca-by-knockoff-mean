# Claim 2 method

Set `d=n`, `X=u 1_n^T`, and `A=q gamma^T`, where `u,q` are independent Haar unit vectors and `gamma_i` are iid Bernoulli(1/5). Then `XX^T/n=uu^T`, whose empirical spectral distribution converges to compactly supported `delta_0`. For the clean eigenvector `u`, write `alpha=<q,u>`, `p_hat=sum(gamma)/n`, and `s=<gamma,1_n>/n=p_hat`. Direct multiplication gives

`(AA^T+AX^T+XA^T)u/n = q(p_hat alpha+s)+u(alpha s)`.

Thus its norm converges in probability to `1/5`, not at rate `n^-1/2`. The independent checker evaluates this closed form. A seeded sweep over six sizes and 200 trials per size checks the finite-size behavior without choosing sizes from the claimed rate.

The negative control replaces `1_n` by an alternating `+1,-1` vector. Then `s=O_p(n^-1/2)`, so the same construction should no longer falsify the rate.
