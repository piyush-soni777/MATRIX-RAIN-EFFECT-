"""
MATRIX RAIN EFFECT - Hollywood Style Terminal Animation
Hollywood's Matrix digital rain effect in your terminal!
"""

import random
import time
import os
import curses
from curses import wrapper

class MatrixRain:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_curses()
        self.drops = []
        self.fonts = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*")
        
    def setup_curses(self):
        """Initialize curses with colors"""
        curses.curs_set(0)  # Hide cursor
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.stdscr.nodelay(True)
        self.stdscr.timeout(50)
        
    def create_drop(self):
        """Create new rain drop"""
        if random.randint(0, 100) < 30:
            x = random.randint(0, self.stdscr.getmaxyx()[1] - 1)
            self.drops.append({
                'x': x,
                'y': 0,
                'chars': [random.choice(self.fonts) for _ in range(random.randint(5, 20))],
                'speed': random.uniform(0.3, 0.8),
                'phase': random.randint(0, 255)
            })
    
    def update_drops(self):
        """Update all rain drops"""
        new_drops = []
        height, width = self.stdscr.getmaxyx()
        
        for drop in self.drops:
            drop['y'] += drop['speed']
            
            # Draw trail
            for i, char in enumerate(drop['chars']):
                if drop['y'] - i >= 0 and drop['y'] - i < height:
                    color = 1 if i == 0 else 2  # Bright head, dim tail
                    try:
                        self.stdscr.addch(int(drop['y'] - i), drop['x'], 
                                        ord(char), curses.color_pair(color))
                    except:
                        pass
            
            # Keep drop if still visible
            if drop['y'] < height + len(drop['chars']):
                new_drops.append(drop)
        
        self.drops = new_drops
    
    def clear_screen(self):
        """Clear screen efficiently"""
        self.stdscr.erase()
        self.stdscr.refresh()
    
    def run(self):
        """Main animation loop"""
        print("🎬 MATRIX RAIN STARTING... Press Ctrl+C to exit")
        time.sleep(1)
        
        try:
            while True:
                self.clear_screen()
                self.create_drop()
                self.update_drops()
                self.stdscr.refresh()
                time.sleep(0.03)
        except KeyboardInterrupt:
            self.stdscr.clear()
            print("\n🌟 Matrix rain stopped!")

def main(stdscr):
    rain = MatrixRain(stdscr)
    rain.run()

if __name__ == "__main__":
    wrapper(main)
