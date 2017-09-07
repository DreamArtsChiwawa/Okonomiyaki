import numpy as np
import matplotlib.pyplot as plt

score_list = [	
				-1.0, -0.9 ,-0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1,
				0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
				0.1, 0.2, 0.2, 0.2, 0.1, 0.5, 0.2, 0.3, 0.3, 0.4, 0.3,
				-0.1, -0.2, -0.2, -0.2, -0.3, -0.3, -0.3, -0.2, -0.2, -0.1
			]

n, bins, patch = plt.hist(score_list, bins=np.arange(-1.0, 1.01, 0.1))

plt.savefig("sample.eps")
plt.show()
