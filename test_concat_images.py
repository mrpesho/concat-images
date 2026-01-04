import argparse
import pytest
from PIL import Image
from concat_images import (
    calculate_canvas_size,
    calculate_position,
    concatenate_images,
    parse_color,
)


def create_test_image(width: int, height: int, color: tuple = (255, 0, 0, 255)) -> Image.Image:
    """Create a solid color test image."""
    return Image.new('RGBA', (width, height), color)


class TestCalculateCanvasSize:
    def test_vertical_same_width(self):
        images = [create_test_image(100, 50), create_test_image(100, 50)]
        width, height = calculate_canvas_size(images, 'vertical', 0)
        assert width == 100
        assert height == 100

    def test_vertical_different_width(self):
        images = [create_test_image(100, 50), create_test_image(200, 50)]
        width, height = calculate_canvas_size(images, 'vertical', 0)
        assert width == 200  # max width
        assert height == 100

    def test_vertical_with_spacing(self):
        images = [create_test_image(100, 50), create_test_image(100, 50)]
        width, height = calculate_canvas_size(images, 'vertical', 10)
        assert width == 100
        assert height == 110  # 50 + 10 + 50

    def test_horizontal_same_height(self):
        images = [create_test_image(50, 100), create_test_image(50, 100)]
        width, height = calculate_canvas_size(images, 'horizontal', 0)
        assert width == 100
        assert height == 100

    def test_horizontal_different_height(self):
        images = [create_test_image(50, 100), create_test_image(50, 200)]
        width, height = calculate_canvas_size(images, 'horizontal', 0)
        assert width == 100
        assert height == 200  # max height

    def test_horizontal_with_spacing(self):
        images = [create_test_image(50, 100), create_test_image(50, 100)]
        width, height = calculate_canvas_size(images, 'horizontal', 10)
        assert width == 110  # 50 + 10 + 50
        assert height == 100

    def test_three_images_vertical(self):
        images = [create_test_image(100, 50) for _ in range(3)]
        width, height = calculate_canvas_size(images, 'vertical', 5)
        assert width == 100
        assert height == 160  # 50 + 5 + 50 + 5 + 50


class TestCalculatePosition:
    def test_vertical_align_begin(self):
        img = create_test_image(50, 50)
        x, y = calculate_position(img, 100, 200, 0, 'vertical', 'begin')
        assert x == 0
        assert y == 0

    def test_vertical_align_center(self):
        img = create_test_image(50, 50)
        x, y = calculate_position(img, 100, 200, 0, 'vertical', 'center')
        assert x == 25  # (100 - 50) / 2
        assert y == 0

    def test_vertical_align_end(self):
        img = create_test_image(50, 50)
        x, y = calculate_position(img, 100, 200, 0, 'vertical', 'end')
        assert x == 50  # 100 - 50
        assert y == 0

    def test_vertical_with_offset(self):
        img = create_test_image(50, 50)
        x, y = calculate_position(img, 100, 200, 60, 'vertical', 'center')
        assert x == 25
        assert y == 60

    def test_horizontal_align_begin(self):
        img = create_test_image(50, 50)
        x, y = calculate_position(img, 200, 100, 0, 'horizontal', 'begin')
        assert x == 0
        assert y == 0

    def test_horizontal_align_center(self):
        img = create_test_image(50, 50)
        x, y = calculate_position(img, 200, 100, 0, 'horizontal', 'center')
        assert x == 0
        assert y == 25  # (100 - 50) / 2

    def test_horizontal_align_end(self):
        img = create_test_image(50, 50)
        x, y = calculate_position(img, 200, 100, 0, 'horizontal', 'end')
        assert x == 0
        assert y == 50  # 100 - 50

    def test_horizontal_with_offset(self):
        img = create_test_image(50, 50)
        x, y = calculate_position(img, 200, 100, 60, 'horizontal', 'center')
        assert x == 60
        assert y == 25


class TestConcatenateImages:
    def test_vertical_basic(self):
        images = [create_test_image(100, 50), create_test_image(100, 50)]
        result = concatenate_images(images, 'vertical', 0, 'center')
        assert result.size == (100, 100)

    def test_horizontal_basic(self):
        images = [create_test_image(50, 100), create_test_image(50, 100)]
        result = concatenate_images(images, 'horizontal', 0, 'center')
        assert result.size == (100, 100)

    def test_with_spacing(self):
        images = [create_test_image(100, 50), create_test_image(100, 50)]
        result = concatenate_images(images, 'vertical', 20, 'center')
        assert result.size == (100, 120)

    def test_preserves_image_content(self):
        red = create_test_image(10, 10, (255, 0, 0, 255))
        blue = create_test_image(10, 10, (0, 0, 255, 255))
        result = concatenate_images([red, blue], 'vertical', 0, 'center')

        # Check top image is red
        assert result.getpixel((5, 5)) == (255, 0, 0, 255)
        # Check bottom image is blue
        assert result.getpixel((5, 15)) == (0, 0, 255, 255)

    def test_rgba_output(self):
        images = [create_test_image(50, 50), create_test_image(50, 50)]
        result = concatenate_images(images, 'vertical', 0, 'center')
        assert result.mode == 'RGBA'

    def test_custom_background(self):
        small = create_test_image(10, 10, (255, 0, 0, 255))
        large = create_test_image(20, 10, (0, 255, 0, 255))
        result = concatenate_images([small, large], 'vertical', 0, 'center', (0, 0, 255, 255))

        # Background should be blue where small image doesn't cover
        assert result.getpixel((0, 0)) == (0, 0, 255, 255)
        assert result.getpixel((19, 0)) == (0, 0, 255, 255)

    def test_transparent_background(self):
        small = create_test_image(10, 10, (255, 0, 0, 255))
        large = create_test_image(20, 10, (0, 255, 0, 255))
        result = concatenate_images([small, large], 'vertical', 0, 'center', (0, 0, 0, 0))

        # Background should be transparent
        assert result.getpixel((0, 0)) == (0, 0, 0, 0)


class TestParseColor:
    def test_rgb(self):
        assert parse_color('255,128,0') == (255, 128, 0, 255)

    def test_rgba(self):
        assert parse_color('255,128,0,128') == (255, 128, 0, 128)

    def test_transparent(self):
        assert parse_color('transparent') == (0, 0, 0, 0)

    def test_with_spaces(self):
        assert parse_color('255, 128, 0, 128') == (255, 128, 0, 128)

    def test_invalid_format(self):
        with pytest.raises(argparse.ArgumentTypeError):
            parse_color('invalid')

    def test_wrong_component_count(self):
        with pytest.raises(argparse.ArgumentTypeError):
            parse_color('255,255')
