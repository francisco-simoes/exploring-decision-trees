# Exploring Decision trees (for regression)

(IN DEVELOPMENT)

## Summary

### Goal:
Make a regression decision tree constructor based on algorithm 8.1 of [Gareth], building from scratch all the functions present in this algorithm.
Allow the functions involved to print the construction steps, so that one can visualize what is happening and gain a deeper understanding. It should be especially useful for someone learning Decision trees from [Gareth] and [Hastie].

### Procedure:
1. Construct a deep unpruned tree using recursive binary splitting.
2. Define a function that prunes the deep unpruned tree using cost-complexity pruning. This process depends on a hyperparameter $\alpha$.
3. Select a good $\alpha$ using $K$-fold cross-validation. Then 1+2 give us the decision tree.
4. Apply to data also analyzed in [Gareth], to make sure our algorithm works.

**Optional printing:*** To implement optional printing, I created a module called simple_logger which can be used to turn a normal function into a function with optional/debug printing, as long as one substitutes all `print()` calls by `log()` calls. You can read more about it and see a simple example in my GitHub repository about the simple_logger module.


## Recursive Binary Splitting

## Tree prunning [Hastie]

The tree $T_0$ created using recursive binary split will probably overfit. The strategy is to simplify the model by finding an appropriate subtree $T$ of $T_0$ by pruning $T$ using *cost-complexity-pruning*, which we'll briefly explain here.

The *cost complexity criterion* is defined by
$$
C_\alpha(T) = \sum_{m=1}^{\vert T \vert} \sum_{i\in I_m} (y_i - \hat{y}_{R_m})^2 + \alpha \vert T \vert
$$

where $\vert T \vert$ is the number of leaves of $T$, $I_m$ is the indexing set of the region $R_m$ (*i.e.* $R_m = \{x_i \in \text{examples}: i\in I_m\}$), $\hat{y}_{R_m}$ is the predicted response in $R_m$ (in our case $\hat{y}_{R_m}$ is just the mean $\mu_{R_m}$), and $\alpha\in \mathbb{R}^+$ controls the size of the tree.

We now want to find the subtree $T_\alpha\subseteq T_0$ that minimizes $C_\alpha(T)$. Notice that for $\alpha = 0$ the minimizing subtree is $T_0$ itself, thus justifying the notation.

It can be shown [Breiman] that for all $\alpha\in\mathbb{R}^+$ there is a unique smallest subtree $T_\alpha$ that minimizes the cost complexity criterion, and to find it one can use *weakest link pruning*: starting from the bottom (the leaves) of the tree $T_0$, undo the split which has less impact (decreases the least) on the $\sum_{m=1}^{\vert T \vert} \sum_{i\in I_m} (y_i - \hat{y}_{R_m})^2$ part of the cost complexity criterion, obtaining a subtree; keep doing this until you're left only with the root of the tree.
This gives us a sequence of subtrees of $T_0$, and it turns out [Breiman] that this sequence must contain $T_\alpha$.

This means that we can simply implement weakest link pruning to obtain a sequence of subtrees and find the one which minimizes $C_\alpha$. That subtree must be $T_\alpha$.

### Cost-complexity criterion

### Weakest-link pruning

In order to define weakest link pruning, we will use the fact that each pair of siblings in the tree correspond exactly to a split:


The algorithm of the weakest link pruning (acting on the tree $T$) will:
   1. prune away one pair of sibling leaves, creating a temporary subtree $T'$ of $T$.
   2. compute the complexity cost criterion of $T'$.
   3. repeat 1,2 for all pairs of sibling leaves.
   4. select the subtree $T'$ with the lowest cost, and do $T=T'$.
   5. repeat 1-4 until $T= \{\mathrm{root}\}$ -- or equivalently until the height of $T$ is 0.



### Cost-complexity pruning

Lastly, we want to select, from the sequence, the tree with the smallest cost.


## Selecting $\alpha$

In order to select a good value for alpha we use $K$-fold cross-validation.

More exactly, given a set of examples and a list of values for $\alpha$ we need to:
1. Divide it in $K$ equal parts/folds.
2. Construct $K$ different pairs (training set, test set) using those parts.
3. For each of those pairs:
    1. Construct the unprunned tree $T^K$.
    2. For each $\alpha$:
        1. Construct the optimal tree $T_{\alpha}$.
        2. Compute the MSE (denoted $\mathrm{MSE}^K_{\alpha}$) on the test set (the $K$-fold we left out of the training set).
4. Compute the cross-validation $\mathrm{MSE}_\alpha$ for the all the values of $\alpha$, which is the average over K of the $\mathrm{MSE}^K_{\alpha}$.
5. Select the $\alpha$ whose $\mathrm{MSE}_\alpha$ is smallest.

## Testing

## References:

1. [Hastie]  
2. [Norvig]
3. [Gareth]
4. [Breiman]

