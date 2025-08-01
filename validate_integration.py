#!/usr/bin/env python3
"""
Validation script for Claude-GitHub integration
"""

import yaml
import os
import sys

def validate_workflow():
    """Validate the Claude workflow configuration"""
    workflow_path = '.github/workflows/claude.yml'
    
    if not os.path.exists(workflow_path):
        print("❌ Claude workflow file not found")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        # Check required fields (handle YAML parsing quirk where 'on' becomes True)
        if 'name' not in workflow:
            print("❌ Missing required field: name")
            return False
        
        if 'on' not in workflow and True not in workflow:
            print("❌ Missing required field: on")
            return False
            
        if 'jobs' not in workflow:
            print("❌ Missing required field: jobs")
            return False
        
        # Check triggers (handle YAML parsing quirk where 'on' becomes True)
        triggers = workflow.get('on') or workflow.get(True)
        if not triggers:
            print("❌ Missing 'on' section")
            return False
        expected_triggers = ['issue_comment', 'pull_request_review_comment', 'issues']
        
        for trigger in expected_triggers:
            if trigger not in triggers:
                print(f"❌ Missing trigger: {trigger}")
                return False
        
        # Check job configuration
        jobs = workflow['jobs']
        if 'claude-response' not in jobs:
            print("❌ Missing claude-response job")
            return False
        
        job = jobs['claude-response']
        
        # Check permissions
        if 'permissions' not in job:
            print("❌ Missing permissions")
            return False
        
        permissions = job['permissions']
        required_permissions = ['contents', 'pull-requests', 'issues']
        for perm in required_permissions:
            if perm not in permissions or permissions[perm] != 'write':
                print(f"❌ Missing or incorrect permission: {perm}")
                return False
        
        # Check steps
        if 'steps' not in job:
            print("❌ Missing steps")
            return False
        
        steps = job['steps']
        step_names = [step.get('name', '') for step in steps]
        
        if 'Checkout repository' not in step_names:
            print("❌ Missing checkout step")
            return False
        
        if 'Run Claude Code' not in step_names:
            print("❌ Missing Claude action step")
            return False
        
        print("✅ Claude workflow configuration is valid")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error validating workflow: {e}")
        return False

def validate_documentation():
    """Validate documentation files"""
    files_to_check = [
        ('README.md', 'README documentation'),
        ('.claude-config.md', 'Claude configuration documentation')
    ]
    
    all_valid = True
    
    for filename, description in files_to_check:
        if not os.path.exists(filename):
            print(f"❌ Missing {description}: {filename}")
            all_valid = False
            continue
        
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            if len(content.strip()) == 0:
                print(f"❌ Empty {description}: {filename}")
                all_valid = False
                continue
            
            # Check for Claude-related content
            if filename == 'README.md':
                if '@claude' not in content:
                    print(f"❌ README missing @claude usage information")
                    all_valid = False
                    continue
                
                if 'Claude AI Integration' not in content:
                    print(f"❌ README missing Claude AI Integration section")
                    all_valid = False
                    continue
            
            print(f"✅ {description} is valid")
            
        except Exception as e:
            print(f"❌ Error reading {description}: {e}")
            all_valid = False
    
    return all_valid

def main():
    """Main validation function"""
    print("🔍 Validating Claude-GitHub Integration...")
    print()
    
    workflow_valid = validate_workflow()
    print()
    
    docs_valid = validate_documentation()
    print()
    
    if workflow_valid and docs_valid:
        print("🎉 All validations passed! Claude-GitHub integration is ready.")
        return 0
    else:
        print("❌ Some validations failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())