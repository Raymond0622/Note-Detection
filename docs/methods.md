# Methods 
The following article provides description on my implementation of Dijkstra's algorithm, SVM

## Terminology
Staff Height: $L$ Number of pixels between staff lines
Pixel Values: $p_i$ Gray scale color of a pixel

## Dijkstra's algorithm

Readers are asked to briefly overview the inner workings of Dijkstra's algorthim. 

We treat each pixel of an image (N x M pixel) as vertices and the edge value connecting adjacent pixels defined by the pixel value of the mentioned adjacent pixels. We always start from the left (0th column) of the image and the final pixel destination would be the same row number on the right most side of the image (Mth-1) image.

<p align="center">
    <img src = "/images/dj_pixel.png" width = '250'>
</p>

The image above shows an example run of the Dijkstra's algorthim. Each square above represent a pixel of an image which also represent a vertex of a "graph". Edges exists between only adjacent nodes. How are exactly the edge between adjcent nodes computed? The edge is determined by the edge function below: $w(p_1, p_2)$ inputs are the pixel values (either 0 or 255) and spits out $2$ if either pixel value is $0$, or else returns $6$. And the $e(l_1, l_2)$ is the final edge function that compute the edge between any two pixels which multiplies $w$ by $3$ if the Euclidean distance between the two pixel is greater than $1$ (i.e diagonally adjacent pixels). I found that these parameters worked best and produced very great results. The rationale behind the latter function is somewhat apparent: staff lines are horizontally, thus we penalize if we traverse vertically. However, the weight function needs some addtional explanation: It's clear that if the two pixels are black, then less penalty should be incurred. However, 

$$
w(p_1, p_2) = 
 \begin{cases} 
      p_1 < 50 \quad \text{and} \quad p_2 < 50 & 2\\
      else & 6 \\
  \end{cases}
$$

$$
e(l_1, l_2) =
 \begin{cases} 
      Euclidean(l_1, l_2) > 1 & w(p_1, p_2) * 3\\
      else &  w(p_1, p_2) \\
  \end{cases}
$$

So, using the example above, the edge weights would be:
* C-N: 6
* C-NE: $6\sqrt{2}$
* C-E: 2
* C-SE: $2\sqrt{2}$
* C-S: 2
and clearly we should not go backwards... And with this simple implemenatation, we get something like this:

<p align="center">
    <img src = "/images/dvorak_2.jpg" width = '250' margin = '50px'>
    <img src = "/images/staff_lines_dvorak_2_naive.jpg" width = '250'>
</p>

That is disgusting! We do see some sort of structure/resemblance of least paths concentrating on the staff lines to traverse from left side of the image to the right side. In the end, we want to predict if truly each black pixels represented above is a staff line by SVM, and we desire to limit the number of pixels to be predicted as prediction stage is the bottleneck process in this first step. 

How do we fix this? There are 3 main steps we will take:

1) Filter out paths that crosses white pixels too often (i.e more than 25% of the total number of pixel in the path)
2) Remove the paths that are close to the left/right edge. Staff lines only start around 4-5 staff height away from the edge
3) Calculate the Pearson correlation coefficient of the paths and sift out coefficients that are too high (i.e 0 means no correlation, i.e, strictly horizontal)

### Step 1
Pretty self-explanatory. Staff lines are strictly made up of dark pixels and since the paths will inevitably traverse white pixels on the left/right most edges of the sheet music, I chose proportion of black pixels of the path to be 75% (or one can start with step 2 and increase the proportion to around 90%)

### Step 2
Again, self-explanatory. Staff lines roughly start with 4-5 staff height (~$5L$) away from the left/right edge of a sheet music. So, we trimm this section of the path out

### Step 3
This step did not improve greatly result. But, this is to limit staff lines that are too steep. Staff lines are horizontal in nature

Ta da....Would you look at that!

<p align="center">
    <img src = "/images/staff_lines_dvorak_2_final.jpg" width = '250'>
</p>
