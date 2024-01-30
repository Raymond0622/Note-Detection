# Methods 
The following article provides description on my implementation of Dijkstra's algorithm, SVM

## Terminology
Staff Height: $L$ Number of pixels between staff lines
Pixel Values: $p_i$ Gray scale color of a pixel

## Dijkstra's algorithm

Readers are asked to briefly overview the inner workings of Dijkstra's algorthim. 

We treat each pixel of an image (N x M pixel) as vertices and the edge value connecting adjacent pixels defined by the pixel value of the mentioned adjacent pixels. We always start from the left (0th column) of the image and the final pixel destination would be the same row number on the right most side of the image (Mth-1) image.

<p align="center">
    <img src = "/images/dj_pixel.png" width = '400'>
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
and clearly we should not go backwards... And with this simple implemenatation... wait the implementation was NOT simple... let's discuss before showcasing the result

### Implementation of Dijkstra's algorithm:

There are two general approach I took: Naive approach, and the more smart data structure approach. Dijkstra's algorithm is a greedy algorthim in that for each loop or decision to pick the next vertex to visit, we must look for the minimum path to the vertices that have not been visited yet. Minimum is a huge problem. We have to look through all the vertices and check for the minimum distance. This is the bottlneck operation in this algorthim. One can naively loop through all vertices and find the minimum which was my first approach and this operation took around 4-5 minutes (on Python) for a single sheet music of size (1600 x 2150 pixel). So, how do we fix this? There are two things we need to consider: Has a vertex been visited? What's the minimum path of unvisited vertices?

Both issues were fixed by using minimum heap. A heap is a a complete binary tree but for the sake of this project. The completeness is the quite necessary (well.. when I implemented it). A minimum heap is a binary tree such that the children of any parent node is always less than or equal to its parent node. So, you can see that the most top-level node will always be the smallest; hence the minimum across all nodes. So, if we allow each node to be a vertex and order the heap by its path length, then we can easily get the minimum vertex.

When we call the minimum value, we will call two functions: get the minimum, and sink down. The first operation is to remove the node since we won't be visting the vertex again. The latter operation is the fill in the void that's been created from removing the top node. So, we move the very last node of the heap (i.e the most right node of the heap, see the picture below for more detail) and move it up. And obviously, this is not a min heap since the top node is now potentially the greatest path length vertex out of all vertices. So, we must perform the sink down operation which is switching node position based on its path length.

<p align="center">
    <img src = "/images/dvorak_2.jpg" width = '400' margin = '50px'>
    <img src = "/images/staff_lines_dvorak_2_naive.jpg" width = '400'>
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
    <img src = "/images/staff_lines_dvorak_2_final.jpg" width = '400'>
</p>

# Support Vector Machine

Radial based function was used as the kernel function which takes in the input (pixel values of the Canny Edge tranformed images, stacked row major wise) into a specific form to be analyzed. There are various Edge detection CNNs algorthims out there (i.e the simple horizontal, vertical line detection as we only desire staff lines and they are inherently horizontal). But, Canny worked the best in this scenario. 

So for each staff line pixel in the least path, roughly 11x11 pixel was extracted from the Canny image (with the center pixel being the least path pixel) and trained. Yes, I created my own dataset and I believe it was roughly around 5,000 images that I had to label.... In the end, the method worked beautifuly as it should...

And the results are:

<p align="center">
    <img src = "/images/example_pre.jpg" width = '400'>
    <img src = "/images/first_step_example.jpg" width = '400'>
</p>

Now, onto the next step: Create music elements. So why did we even bother removing the staff lines? It's to create music elements that are "islands" of black pixels. DBSCAN will help us identify different islands depending on number of black pixels in the vicinity of a candidate pixel. I suggest reading up on how DBSCAN works why this was used. In short, DBSCAN is great at detecting clusters of arbitrary shape and since music elements are of random shape (i.e clefs, note heads, rest symbols, accidentals, etc), DBSCAN is best. 

We need "islands" to narrows our search area of note heads. If we naively created data sets for SVM to go through every pixel of an image, this would be highly inefficient. So, we partition the image into music elements which MIGHT have note heads. So, we are moving large empty white spaces that we surely know won't have any note heads! So, we first needed to get rid of staff lines since staff lines connect (via path of black pixels) various music elements together. Staff lines could have been kept if we used a different (eps, min) DBSCAN parameter, but this was not explored. Perhaps, something to look into the future.

Anyhow, using DBSCAN with the following parameters:

```python
clustering = DBSCAN(eps=2, min_samples=1).fit(X)
```

where the distance is defined to be the Euclidean distance between pixels. So we just check within a pixel square radius (since diagonal pixels are of radius 1.41, see first picture above). And if a single element is black, then we include it as a core sample! So, what are the results?


<p align="center">
    <img src = "/images/DBSCAN.png" width = '400'>
</p>

Very pretty! So, now what's next? We box around each music element and create bounding boxes to be fed into the notehead SVM by taking the min/max pixels of each cluster. After such...

<p align="center">
    <img src = "/images/music_parts_box.png" width = '400'>
</p>







