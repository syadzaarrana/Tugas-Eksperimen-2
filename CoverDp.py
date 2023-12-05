def dfs(adj, dp, src, par, cover):
    for child in adj[src]:
        if child != par:
            dfs(adj, dp, child, src, cover)

    for child in adj[src]:
        if child != par:
            dp[src][0] = dp[child][1] + dp[src][0]
            dp[src][1] = dp[src][1] + min(dp[child][1], dp[child][0])

    if dp[src][0] < dp[src][1]:
        cover[src] = 0
    else:
        cover[src] = 1

def min_size_vc(adj):
    N = len(adj)
    dp = [[0 for j in range(2)] for i in range(N+1)]
    cover = [0] * (N+1)

    for i in range(1, N+1):
        dp[i][0] = 0
        dp[i][1] = 1

    dfs(adj, dp, 1, -1, cover)

    cover = [i for i, val in enumerate(cover) if val == 1]

    if min(dp[1][0], dp[1][1]) == len(cover):
        return cover

def vc_dp(adj):
    vc = min_size_vc(adj)
    return vc, len(vc)
