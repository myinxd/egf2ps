# egf2ps
Since most sources with high temperature (brightness) in our Universe are point or point-like, design of approach to detect those point sources at different frequency bands are of great significant. In this repository, a module prepared by python is provided, which aims at detecting point sources in X-ray astronomical images. 

There are three different reasons motivating us to do this work, which are briefly listed as follows,

- The foreground stars do not radiate X rays so that the distant faint point sources can be detected.
- Point-like sources, especially the black holes radiate strong X rays.
- Many matural observatories were launched, e.g. [Chandra](https://cxc.harvard.edu), [XMM-Newton](http://www.cosmos.esa.int/web/xmm-newton) and [Suzaku](http://www.cosmos.esa.int/web/suzaku), thus large amount of samples can be fetched.

However, there are still some difficulties hindering our detections,

- Most of point sources are faint as bright as the backgrounds, as they are quiet far from us.
- Restrctied with exposure times (observing time), detected phontons are usually short, thus Poisson shock noises are generated.
- The noise from obsever itself, combined with point spread effections also blurred the images.

Above all, to handle this difficulties, precisely detect and extract the point sources, an approach is proposed. A group of multi-scale filters are designed by the two dimensional (2D) Gaussian functions. We have found that the 2D Gaussian filter can not only perform as a low-pass filter, but also be a template to match the elliptical or circular point sources.  With help of the proposed approach, the point sources will be located and extracted.

The mainly scripts for our elliptical Gaussian filters to detect point sources (egf2ps) is provided, and we very welcome you to utlize them in your works. The license is also discribed and listed at the end of the readme.

## How to use it?
The scrips are prepared under grammar of the [python3](https://en.wikipedia.org/wiki/Python_(programming_language)), and some basic official modules and astrophycial modules are required. They are listed as follows,

- NumPy, SciPy : process with ndarray formation data and do the concolusion calculations
- astropy, pyregion : process on the astronomical image files (.fits) and region files (.reg).
- matplotlib: display results and read or save images
- pandas: save the PS list as `csv` files

The simplest way to use the egf2ps package to detect point sources is to install it, and process at the command line.
- Install
```sh
   $ cd egf2ps
   $ pip install --user .
```
- Run detection
```sh
   $ egf2ps <confpath>
```
The configuration file holding `input`,`output`,`filter`,`peaks`,and `snr` pararmeters should be provided, a [template](https://github.com/myinxd/egf2ps/egf2ps/configs/confspec.conf) can be referred. 
## Author
- Zhixian MA <`zxma_sjtu(at)qq.com`>

## License
Unless otherwise declared:

- Codes developed are distributed under the [MIT license](https://opensource.org/licenses/mit-license.php);
- Documentations and products generated are distributed under the [Creative Commons Attribution 3.0 license](https://creativecommons.org/licenses/by/3.0/us/deed.en_US);
- Third-party codes and products used are distributed under their own licenses.
