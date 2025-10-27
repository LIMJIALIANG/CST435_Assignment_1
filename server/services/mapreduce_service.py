"""
MapReduce Service Implementation
Performs parallel counting of CGPA ranges and grade distributions
"""

import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor


class MapReduceService:
    """
    Implements MapReduce pattern for student data analysis
    """
    
    @staticmethod
    def map_cgpa(student):
        """Map function: categorize CGPA into ranges"""
        cgpa = student.cgpa
        if cgpa >= 3.75:
            return ("3.75-4.00", 1)
        elif cgpa >= 3.50:
            return ("3.50-3.74", 1)
        elif cgpa >= 3.00:
            return ("3.00-3.49", 1)
        elif cgpa >= 2.50:
            return ("2.50-2.99", 1)
        else:
            return ("0.00-2.49", 1)
    
    @staticmethod
    def map_grade(student):
        """Map function: extract grade"""
        return (student.grade, 1)
    
    @staticmethod
    def reduce_counts(mapped_data):
        """Reduce function: aggregate counts"""
        result = defaultdict(int)
        for key, value in mapped_data:
            result[key] += value
        return dict(result)
    
    @staticmethod
    def perform_mapreduce(students, operation):
        """
        Perform MapReduce operation on student data
        
        Args:
            students: List of student objects
            operation: "cgpa_count" or "grade_count"
        
        Returns:
            Dictionary with counts and processing time
        """
        start_time = time.time()
        
        # Map phase - parallel processing
        with ThreadPoolExecutor(max_workers=4) as executor:
            if operation == "cgpa_count":
                mapped_data = list(executor.map(MapReduceService.map_cgpa, students))
            elif operation == "grade_count":
                mapped_data = list(executor.map(MapReduceService.map_grade, students))
            else:
                raise ValueError(f"Unknown operation: {operation}")
        
        # Reduce phase
        result = MapReduceService.reduce_counts(mapped_data)
        
        processing_time = time.time() - start_time
        
        print(f"[MapReduce] Operation: {operation}")
        print(f"[MapReduce] Processed {len(students)} students")
        print(f"[MapReduce] Results: {result}")
        print(f"[MapReduce] Processing time: {processing_time:.4f} seconds")
        
        return {
            'result': result,
            'processing_time': processing_time
        }
