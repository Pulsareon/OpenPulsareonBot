#!/usr/bin/env python3
"""
RAW10 (MIPI CSI-2 packed format) processing utilities.

This module implements packing and unpacking of RAW10 data format commonly used
in MIPI CSI-2 camera interfaces. RAW10 packs 4 pixels into 5 bytes.
"""

import numpy as np
from typing import Tuple, Union


def pack_raw10(image: np.ndarray) -> bytes:
    """
    Pack 16-bit image (0-1023) into RAW10 byte stream.
    
    RAW10 format packs 4 pixels into 5 bytes:
    Byte 0: [Pixel0 bits 9:2]
    Byte 1: [Pixel1 bits 9:2]
    Byte 2: [Pixel2 bits 9:2]
    Byte 3: [Pixel3 bits 9:2]
    Byte 4: [Pixel3:1:0 bits 1:0, Pixel2:1:0 bits 1:0, Pixel1:1:0 bits 1:0, Pixel0:1:0 bits 1:0]
    
    Args:
        image: 2D numpy array of uint16 values (0-1023)
        
    Returns:
        bytes: Packed RAW10 byte stream
        
    Raises:
        ValueError: If image values are outside 0-1023 range
    """
    if image.dtype != np.uint16:
        raise ValueError("Image must be uint16 type")
    
    if np.any(image > 1023):
        raise ValueError("Image values must be in range 0-1023")
    
    height, width = image.shape
    
    # Reshape image to process in groups of 4 pixels
    flat_image = image.flatten()
    
    # Pad with zeros to make length divisible by 4
    pad_length = (4 - (len(flat_image) % 4)) % 4
    padded_image = np.pad(flat_image, (0, pad_length), mode='constant')
    
    # Reshape into groups of 4 pixels
    pixel_groups = padded_image.reshape(-1, 4)
    
    # Pack each group of 4 pixels into 5 bytes
    byte_stream = bytearray()
    
    for group in pixel_groups:
        # Extract bits 9:2 from each pixel (8 bits each)
        byte0 = (group[0] >> 2) & 0xFF
        byte1 = (group[1] >> 2) & 0xFF
        byte2 = (group[2] >> 2) & 0xFF
        byte3 = (group[3] >> 2) & 0xFF
        
        # Pack bits 1:0 from all 4 pixels into one byte
        # Format: [P3:1:0, P2:1:0, P1:1:0, P0:1:0]
        lsb_byte = (
            ((group[3] & 0x03) << 6) |  # Pixel3 bits 1:0 at positions 7:6
            ((group[2] & 0x03) << 4) |  # Pixel2 bits 1:0 at positions 5:4
            ((group[1] & 0x03) << 2) |  # Pixel1 bits 1:0 at positions 3:2
            (group[0] & 0x03)           # Pixel0 bits 1:0 at positions 1:0
        )
        
        byte_stream.extend([byte0, byte1, byte2, byte3, lsb_byte])
    
    return bytes(byte_stream)


def unpack_raw10(byte_stream: bytes, width: int, height: int) -> np.ndarray:
    """
    Unpack RAW10 byte stream back to 16-bit image.
    
    Args:
        byte_stream: Packed RAW10 bytes
        width: Original image width
        height: Original image height
        
    Returns:
        np.ndarray: 2D uint16 image (0-1023)
        
    Raises:
        ValueError: If byte stream length doesn't match expected size
    """
    expected_bytes = (width * height * 5) // 4
    if len(byte_stream) != expected_bytes:
        raise ValueError(f"Expected {expected_bytes} bytes for {width}x{height} image, "
                       f"got {len(byte_stream)} bytes")
    
    # Process in groups of 5 bytes (4 pixels)
    pixel_count = width * height
    result = np.zeros(pixel_count, dtype=np.uint16)
    
    for i in range(0, len(byte_stream), 5):
        byte0, byte1, byte2, byte3, lsb_byte = byte_stream[i:i+5]
        
        # Extract LSB bits from the packed byte
        lsb0 = lsb_byte & 0x03        # Pixel0 bits 1:0
        lsb1 = (lsb_byte >> 2) & 0x03  # Pixel1 bits 1:0
        lsb2 = (lsb_byte >> 4) & 0x03  # Pixel2 bits 1:0
        lsb3 = (lsb_byte >> 6) & 0x03  # Pixel3 bits 1:0
        
        # Reconstruct 10-bit values
        pixel0 = (byte0 << 2) | lsb0
        pixel1 = (byte1 << 2) | lsb1
        pixel2 = (byte2 << 2) | lsb2
        pixel3 = (byte3 << 2) | lsb3
        
        # Store in result array
        group_idx = i // 5 * 4
        result[group_idx:group_idx+4] = [pixel0, pixel1, pixel2, pixel3]
    
    # Reshape to original dimensions and remove padding if any
    return result[:pixel_count].reshape(height, width)


def validate_raw10_roundtrip():
    """Validate pack->unpack roundtrip with random test data."""
    print("Testing RAW10 pack/unpack roundtrip...")
    
    # Test various image sizes
    test_sizes = [(64, 64), (128, 128), (256, 256), (512, 512), (1024, 768)]
    
    for width, height in test_sizes:
        print(f"Testing {width}x{height} image...")
        
        # Generate random 10-bit image data
        original = np.random.randint(0, 1024, size=(height, width), dtype=np.uint16)
        
        # Pack to RAW10
        packed = pack_raw10(original)
        
        # Verify packed size
        expected_packed_size = (width * height * 5) // 4
        assert len(packed) == expected_packed_size, \
            f"Packed size mismatch: expected {expected_packed_size}, got {len(packed)}"
        
        # Unpack back
        reconstructed = unpack_raw10(packed, width, height)
        
        # Verify data integrity
        assert original.shape == reconstructed.shape, \
            f"Shape mismatch: {original.shape} vs {reconstructed.shape}"
        
        assert np.array_equal(original, reconstructed), \
            f"Data mismatch for {width}x{height} image"
        
        print(f"  PASS {width}x{height}: Packed {len(packed)} bytes, data integrity verified")
    
    print("All tests passed!")


def test_edge_cases():
    """Test edge cases and error conditions."""
    print("Testing edge cases...")
    
    # Test invalid values
    try:
        invalid_image = np.array([[1024]], dtype=np.uint16)  # Value > 1023
        pack_raw10(invalid_image)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  PASS Correctly rejected value > 1023")
    
    # Test wrong dtype
    try:
        wrong_dtype = np.array([[255]], dtype=np.uint8)
        pack_raw10(wrong_dtype)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  PASS Correctly rejected wrong dtype")
    
    # Test wrong byte stream size
    try:
        unpack_raw10(b'\x00' * 10, 4, 4)  # Should need 5 bytes for 4 pixels
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  PASS Correctly rejected wrong byte stream size")
    
    print("Edge case tests passed!")


if __name__ == "__main__":
    """
    Main test routine for RAW10 processing.
    """
    print("=" * 60)
    print("RAW10 MIPI CSI-2 Format Processing Test")
    print("=" * 60)
    
    # Run comprehensive validation
    validate_raw10_roundtrip()
    print()
    test_edge_cases()
    
    print("\n" + "=" * 60)
    print("All RAW10 processing tests completed successfully!")
    print("=" * 60)