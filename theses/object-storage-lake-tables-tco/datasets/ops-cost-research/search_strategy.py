#!/usr/bin/env python3
"""
Search strategy for operational cost data related to data platforms.
Focus on FTE time allocation, maintenance overhead, and operational metrics.
"""

import requests
import json
import csv
import time
from datetime import datetime
import os

class OpsDataHunter:
    def __init__(self):
        self.search_terms = [
            # Direct operational cost terms
            "database administrator time allocation study",
            "devops cost data platform staffing",
            "platform engineering operational overhead",
            "data team fte allocation metrics",
            "database maintenance time tracking",
            "data warehouse operational costs",
            
            # Industry survey terms
            "database administration salary survey operational",
            "data platform staffing requirements study",
            "database operational overhead benchmark",
            "data engineering team productivity metrics",
            
            # Academic/research terms
            "database system administration cost analysis",
            "operational database management time study",
            "data platform total cost ownership",
            "database maintenance labor requirements",
            
            # Specific metric terms
            "fte hours per terabyte database",
            "database tables per administrator ratio",
            "data platform oncall time allocation",
            "database incident response time metrics",
            
            # Case study terms
            "database consolidation operational savings",
            "data platform migration cost analysis",
            "database operational efficiency case study",
            "data warehouse administration overhead"
        ]
        
        self.file_search_terms = [
            'filetype:csv "database" "operational" "fte"',
            'filetype:xlsx "data platform" "staffing" "hours"',
            'filetype:pdf "database administration" "time allocation"',
            'site:gartner.com "database" "operational cost"',
            'site:forrester.com "data platform" "staffing"',
            'site:stackoverflow.com "database administration" "time"',
            'site:reddit.com/r/sysadmin "database" "operational overhead"',
            'site:reddit.com/r/devops "data platform" "maintenance"'
        ]
        
        self.target_sources = [
            "gartner.com",
            "forrester.com", 
            "idc.com",
            "oreilly.com",
            "dataversity.net",
            "databasejournal.com",
            "zdnet.com",
            "computerworld.com",
            "infoworld.com",
            "datanami.com",
            "stackoverflow.com",
            "reddit.com",
            "github.com",
            "medium.com",
            "dev.to",
            "kaggle.com",
            "datasets.google.com"
        ]
    
    def generate_search_urls(self):
        """Generate search URLs for different platforms"""
        urls = []
        
        # Google search URLs
        for term in self.search_terms[:10]:  # Limit to avoid too many requests
            encoded_term = term.replace(" ", "+")
            urls.append(f"https://www.google.com/search?q={encoded_term}")
        
        # File-specific searches
        for term in self.file_search_terms:
            encoded_term = term.replace(" ", "+")
            urls.append(f"https://www.google.com/search?q={encoded_term}")
            
        return urls
    
    def save_search_plan(self):
        """Save the search strategy to file"""
        plan = {
            "search_terms": self.search_terms,
            "file_search_terms": self.file_search_terms,
            "target_sources": self.target_sources,
            "target_metrics": [
                "fte_hours_per_month",
                "tables_managed",
                "terabytes_managed", 
                "incident_count",
                "oncall_hours",
                "maintenance_hours",
                "upgrade_hours",
                "org_size",
                "stack_type"
            ],
            "generated_at": datetime.now().isoformat()
        }
        
        with open("ops_cost_search_plan.json", "w") as f:
            json.dump(plan, f, indent=2)
        
        print(f"Search plan saved with {len(self.search_terms)} search terms")
        print(f"Targeting {len(self.target_sources)} source types")

if __name__ == "__main__":
    hunter = OpsDataHunter()
    hunter.save_search_plan()