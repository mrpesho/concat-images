# concat-images

Combine multiple images into one with customizable orientation, spacing, and alignment.

## Installation

```bash
pip install -r requirements.txt
```

## Python Usage

```python
from concat_images import load_images, concatenate_images

images = load_images(['a.png', 'b.png', 'c.png'])
result = concatenate_images(images, orientation='horizontal', spacing=10, alignment='center')
result.save('output.png')
```

## CLI Usage

```bash
./concat_images.py output.png img1.png img2.png [img3.png ...]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --orientation` | `vertical` or `horizontal` | `vertical` |
| `-s, --space` | Pixels between images | `0` |
| `-a, --align` | `begin`, `center`, or `end` | `center` |

### Example

```bash
./concat_images.py result.png a.png b.png c.png -o horizontal -s 10 -a center
```
