"""
MapReduce Service Implementation
Performs parallel counting of CGPA ranges based on grade scale
"""

import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor


class MapReduceService:
    """
    Implements MapReduce pattern for student data analysis
    Based on official grading scale with CGPA ranges
    """
    
    @staticmethod
    def map_cgpa(student):
        """
        Map function: categorize students by CGPA range
        Returns grade category with CGPA range based on grading scale
        
        Grade Scale:
        A: 3.68-4.00
        A-: 3.50-3.67
        B+: 3.33-3.49
        B: 3.00-3.32
        B-: 2.83-2.99
        C+: 2.67-2.82
        C: 2.50-2.66
        C-: 2.33-2.49
        D+: 2.17-2.32
        D: 2.00-2.16
        D-: 1.67-1.99
        F: 0.00-1.66
        """
        cgpa = student.cgpa
        if cgpa >= 3.68:
            return ("A (3.68-4.00)", 1)
        elif cgpa >= 3.50:
            return ("A- (3.50-3.67)", 1)
        elif cgpa >= 3.33:
            return ("B+ (3.33-3.49)", 1)
        elif cgpa >= 3.00:
            return ("B (3.00-3.32)", 1)
        elif cgpa >= 2.83:
            return ("B- (2.83-2.99)", 1)
        elif cgpa >= 2.67:
            return ("C+ (2.67-2.82)", 1)
        elif cgpa >= 2.50:
            return ("C (2.50-2.66)", 1)
        elif cgpa >= 2.33:
            return ("C- (2.33-2.49)", 1)
        elif cgpa >= 2.17:
            return ("D+ (2.17-2.32)", 1)
        elif cgpa >= 2.00:
            return ("D (2.00-2.16)", 1)
        elif cgpa >= 1.67:
            return ("D- (1.67-1.99)", 1)
        else:
            return ("F (0.00-1.66)", 1)
    
    @staticmethod
    def reduce_counts(mapped_data):
        """Reduce function: aggregate counts"""
        result = defaultdict(int)
        for key, value in mapped_data:
            result[key] += value
        return dict(result)
    
    @staticmethod
    def perform_mapreduce(students):
        """
        Perform MapReduce operation on student data for CGPA classification
        
        Args:
            students: List of student objects
        
        Returns:
            Dictionary with counts and processing time
        """
        start_time = time.time()
        
        # Map phase - parallel processing
        with ThreadPoolExecutor(max_workers=4) as executor:
            mapped_data = list(executor.map(MapReduceService.map_cgpa, students))
        
        # Reduce phase
        result = MapReduceService.reduce_counts(mapped_data)
        
        # Sort results by grade order
        grade_order = [
            "A (3.68-4.00)", "A- (3.50-3.67)", "B+ (3.33-3.49)", "B (3.00-3.32)",
            "B- (2.83-2.99)", "C+ (2.67-2.82)", "C (2.50-2.66)", "C- (2.33-2.49)",
            "D+ (2.17-2.32)", "D (2.00-2.16)", "D- (1.67-1.99)", "F (0.00-1.66)"
        ]
        sorted_result = {grade: result[grade] for grade in grade_order if grade in result}
        
        processing_time = time.time() - start_time
        
        return {
            'cgpa_classification': sorted_result,
            'processing_time': processing_time
        }
