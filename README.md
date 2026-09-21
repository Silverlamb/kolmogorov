# Approximating a Non-Computable function, Kolmogorov Complexity
$$K(x) = min_{p \in \Pi}\{|p|: U(p, \epsilon)= x\}$$
The equation above sets off a multitude of important theoretical questions in the realm of computer complexity. $K(x)$ represents the Kolmogorov complexity, a function whose input is an arbitrary string $x$ and output is the minimum length program, that runs on a universal Turing machine, whose output is the string $x$. Essentially, we are looking for the most compressible representation for our string $x$. There are nice properties that are expected when plotting the function on a cartesian graph. However, the Kolmogorov Complexity has been proven to be uncomputable due to halting. While such a graph can not fully computed, an approximation of the graph is possible. The only question is how close can we get to the true $K(x)$? The following will describe the approach we took to approximating $K(x)$.
## Graph
Most strings are incompressible due to the incompressible theorem; so, sampling random strings to show the compression dips would take an incredibly long time especially as our string size grows. This is troublesome for our graph because we may leave out key compression details that gives $K(x)$ its shape. To deal with this, we should generate strings with patterns. Strings with patterns can purposefully be generated with the decompressor modern day compressors like Zip gives us. For instance take a look at the string:
$$100110$$
Assuming this string is completely random, we have reached a block of incompressibility that can do no better than $\log_2{n}$, where $n$ is the length of the string. However, what if we took this block and repeated it by raising it to a power?
$$100110^{n}$$
We have effectively made a string with a pattern that is compressible (on purpose, with our compressor). Now, consider what could be the most compressible string: $1^n$. We know this string is incredibly compressible. We can use these compressible strings and then build our graph around them by sampling points that are close to these incredibly compressible strings and also sampling random points to represent where most of the strings lie. We will call our approximation $K(x)_{approx}$. One thing to note is $K(x) \leq K(x)_{approx}$ since our approximation can either be as good as $K(x)$ or worse.

So, now we get an image that looks like this: 
![[compression_plot_linear_orange.png]]
We can see the graph dips down onto our very compressible strings and gradually increase. We can also see the logarithmic trend that we expect for incompressible strings (most strings) in red. Turns out most randomly generated strings (or as random as we can make them) as the proof for incompressibility goes.

Let's look at the formal properties that $K(x)$ exhibits (such are distilled from Professor Abrahim Ladha's notes):
- $K(x)$ grows unbounded
- $K(x)$ "hugs" log. This expected as a random string can really only be compressible in the smallest form of encoding we can get it (the binary representation of that string)
- $K(x)$ dips infinitely often. This is expect because there are strings, though very few, that will be incredibly compressible to its counterpart strings. 
- $K(x)$ has continuous properties. This is most jarring, since we know $K(x)$ to be discrete. This, however, the notion of a smooth curve can be applied to discrete values as well.

We can try running an approximation model through our points to show a bit of continuity and model $K(X)$ as a continuous function. Lets apply some polynomial regression on on our data. Here is what we get for 3, 5, and 15 degrees respectively.
![[compression_regression.png]]
![[compression_regression 3.png]]![[compression_regression 4.png]]
We see that our graph may be getting smoother yet we don't the exact sharp, jagged dip visualizations that we expect. So lets try some other graph approximation techniques.

So lets try a lower envelope approximation (rolling minimum). Here is what we get.![[compression_envelope.png]]
This method is providing real shape our data points. Maybe we can smooth this out? Lets try applying Savitzky-Golay.![[compression_smoothed_envelope.png]]
Between the two images now, it is easier to see our approximation graph now.

## Program Notes
- `pattern_flip*.py` is the family of programs that represents the initial $K(x)_{approx}$ graphs
- `compress.py` contains statistical tests with compression (like with Zip)
- `BB.py` is a program that generates Turing Machines and their outputs

## Thoughts for the Graph & Writing (unedited)
### TODO
- Fix legend for polynomial graphs (degrees used)
### Thoughts
Some more thoughts: I wish that we can really show those more extreme dips. Maybe we could incorporate Savitzky-Golay and our rolling minimum as a mixture to show sharp edges when they exist and smoothness when we have lots of points in a local area. Also, for data points we would like to make even larger strings and potentially find smaller Turing machines. Lets try Busy Beaver and generate some really large strings that may be random but are just small encoded Turing machines that can present such a pattern. Maybe this could contribute to the graph. We can also try to find such Turing machines maybe efficiently? There was a paper that was related in finding large busy beaver candidates. What if we made an automated machine that is linked to compression? After all compression and intelligences are related. Maybe try to use an llm that maybe produces compressed strings or strings with patterns but remember that the model is generally bigger.So why couldn't we take an intelligent thing and have it compress bits of information? 

Some things to note is that when we are computing this approximation, we are essentially showing an upper bound for the the true k(x). Yet we still don't know if the K(x) we are showing really is a relatively close image to the true k(x). We might need to introduce a bound or confidence interval or some kind of Chernoff bound on how far the estimation itself is from the true k(x). We could provably show up to 5 TM states as maybe a lower bound. The minimum size program on the universal turing machine. So we may be able to show large values fall under the size of that in comparison to other random values. 

Another interesting thing to consider the line that follows most strings (that are incompressible). As we grow our string, we should even expect our randomly generated incompressible strings to expand in variance for compressibility because long incompressible strings will have small patterns embedded into them. We should see a shift in width as we go up in $n$. Also can we provably show that $1^n$ is the most compressible string? Busy beaver (nlogn what is g)? Crowd source stuff.