#!/usr/bin/env python3
"""
Skills CLI - Load context documentation as "skills" for VS Code shortcuts
"""

import json
import sys
from pathlib import Path
import argparse
import pyperclip  # For clipboard operations
import subprocess
import os


class SkillsManager:
    def __init__(self, manifest_path="context/manifest.json"):
        self.base_dir = Path(__file__).parent
        self.manifest_path = self.base_dir / manifest_path
        self.manifest = self._load_manifest()
    
    def _load_manifest(self):
        """Load the skills manifest"""
        if not self.manifest_path.exists():
            print(f"Error: Manifest not found at {self.manifest_path}", file=sys.stderr)
            sys.exit(1)
        
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_skills(self):
        """List all available skills"""
        print("Available Skills:")
        print("=" * 60)
        for doc in self.manifest.get('docs', []):
            path = doc['path']
            keywords = ', '.join(doc['when'])
            skill_name = Path(path).stem
            print(f"\n📚 {skill_name}")
            print(f"   Path: {path}")
            print(f"   Keywords: {keywords}")
        print("\n" + "=" * 60)
        print(f"Total: {len(self.manifest.get('docs', []))} skills")
    
    def get_skill_by_name(self, skill_name):
        """Find a skill by its name"""
        skill_name_lower = skill_name.lower()
        for doc in self.manifest.get('docs', []):
            if Path(doc['path']).stem.lower() == skill_name_lower:
                return doc
        return None
    
    def load_skill(self, skill_name, output='copilot'):
        """Load a skill and output it"""
        skill = self.get_skill_by_name(skill_name)
        if not skill:
            print(f"Error: Skill '{skill_name}' not found", file=sys.stderr)
            print("\nAvailable skills:", file=sys.stderr)
            for doc in self.manifest.get('docs', []):
                print(f"  - {Path(doc['path']).stem}", file=sys.stderr)
            sys.exit(1)
        
        skill_path = self.base_dir / skill['path']
        if not skill_path.exists():
            print(f"Error: Skill file not found at {skill_path}", file=sys.stderr)
            sys.exit(1)
        
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if output == 'copilot':
            # Save to temp file and open in Copilot chat using #file reference
            temp_file = self.base_dir / '.copilot_context.md'
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(f"# Context: {skill_name}\n\n{content}")
            
            # Open the temp file in editor (Copilot can reference it)
            try:
                subprocess.run(['code', str(temp_file)], check=True, 
                             capture_output=True, timeout=5)
                print(f"✓ Skill '{skill_name}' loaded ({len(content)} chars)")
                print(f"  Opening in editor for Copilot context...")
                print(f"  Use @workspace or reference this file in Copilot chat")
            except subprocess.TimeoutExpired:
                print(f"✓ Skill '{skill_name}' saved to {temp_file}")
                print(f"  File opened in editor for Copilot context")
            except Exception as e:
                print(f"Note: Saved to {temp_file}")
                print(f"  You can reference it in Copilot with @workspace")
        elif output == 'clipboard':
            pyperclip.copy(content)
            print(f"✓ Skill '{skill_name}' loaded to clipboard ({len(content)} chars)")
            print(f"  Use Ctrl+V to paste into Copilot chat")
        elif output == 'stdout':
            print(content)
        elif output == 'file':
            temp_file = self.base_dir / '.skill_temp.md'
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Skill '{skill_name}' written to {temp_file}")
        
        return content
    
    def show_skill(self, skill_name):
        """Show skill content directly"""
        self.load_skill(skill_name, output='stdout')


def main():
    parser = argparse.ArgumentParser(
        description='Skills CLI - Load context documentation for Copilot',
        epilog='Examples:\n'
               '  skills.py list                    # List all skills\n'
               '  skills.py load GTest_Mock         # Load Google Mock skill to clipboard\n'
               '  skills.py show GTest_Execute      # Display skill content\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    subparsers.add_parser('list', help='List all available skills')
    
    # Load command
    load_parser = subparsers.add_parser('load', help='Load a skill for Copilot')
    load_parser.add_argument('skill_name', help='Name of the skill to load')
    load_parser.add_argument('--output', choices=['copilot', 'clipboard', 'stdout', 'file'],
                           default='copilot', help='Output destination (default: copilot)')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show skill content')
    show_parser.add_argument('skill_name', help='Name of the skill to show')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = SkillsManager()
    
    if args.command == 'list':
        manager.list_skills()
    elif args.command == 'load':
        manager.load_skill(args.skill_name, output=args.output)
    elif args.command == 'show':
        manager.show_skill(args.skill_name)


if __name__ == '__main__':
    main()
