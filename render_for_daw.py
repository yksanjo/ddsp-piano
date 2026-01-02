#!/usr/bin/env python3
"""
Helper script to render MIDI files with DDSP-Piano for use in DAWs.
This creates audio files that can be imported into your DAW as audio tracks.
"""

import argparse
import os
from synthesize_midi_file import main as synthesize_main, process_args as synth_process_args
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Render MIDI files to audio for DAW import",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Render a single MIDI file
  python render_for_daw.py input.mid output.wav
  
  # Render with specific piano model
  python render_for_daw.py input.mid output.wav --piano_type 5
  
  # Render without reverb (dry signal)
  python render_for_daw.py input.mid output.wav --unreverbed
        """
    )
    
    # Reuse arguments from synthesize_midi_file.py
    parser.add_argument('-c', '--config', type=str, 
                        default='ddsp_piano/configs/maestro-v2.gin',
                        help="Model config file")
    parser.add_argument('--ckpt', type=str, 
                        default='ddsp_piano/model_weights/v2/',
                        help="Model checkpoint")
    parser.add_argument('--piano_type', type=int, default=9,
                        help="Piano model (0-9, default: 9)")
    parser.add_argument('-wu', '--warm_up', type=float, default=0.5,
                        help="Warm-up duration in seconds")
    parser.add_argument('-d', '--duration', type=float, default=None,
                        help="Maximum duration (None = full file)")
    parser.add_argument('-n', '--normalize', type=float, default=-3.0,
                        help="Normalize to dBFS (default: -3.0)")
    parser.add_argument('-u', '--unreverbed', action='store_true',
                        help="Also generate dry audio")
    parser.add_argument('midi_file', type=str, help="Input MIDI file")
    parser.add_argument('out_file', type=str, help="Output WAV file")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.midi_file):
        print(f"Error: MIDI file not found: {args.midi_file}")
        sys.exit(1)
    
    print(f"Rendering {args.midi_file} to {args.out_file}")
    print(f"Using piano model: {args.piano_type}")
    if args.normalize:
        print(f"Normalizing to: {args.normalize} dBFS")
    
    # Call the synthesis function
    try:
        synthesize_main(args)
        print(f"\n✓ Successfully rendered: {args.out_file}")
        print(f"\nYou can now import this audio file into your DAW!")
        if args.unreverbed:
            print(f"  Dry version: {args.out_file}_unreverbed.wav")
    except Exception as e:
        print(f"\n✗ Error during synthesis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

























