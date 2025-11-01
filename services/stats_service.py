"""
Statistical Analysis Service Implementation
Performs comprehensive statistical analysis on student data
"""

import time
from collections import defaultdict


class StatsService:
    """
    Implements statistical analysis for student marks
    """
    
    @staticmethod
    def calculate_avg_cgpa_by_faculty(students):
        """Calculate average CGPA per faculty"""
        faculty_data = defaultdict(lambda: {'total_cgpa': 0, 'count': 0})
        
        for student in students:
            faculty_data[student.faculty]['total_cgpa'] += student.cgpa
            faculty_data[student.faculty]['count'] += 1
        
        result = []
        for faculty, data in faculty_data.items():
            avg_cgpa = data['total_cgpa'] / data['count']
            result.append({
                'faculty': faculty,
                'average_cgpa': avg_cgpa,
                'student_count': data['count']
            })
        
        return result
    
    @staticmethod
    def calculate_grade_distribution(students):
        """Calculate grade distribution with percentages"""
        grade_counts = defaultdict(int)
        total_students = len(students)
        
        for student in students:
            grade_counts[student.grade] += 1
        
        result = []
        for grade, count in sorted(grade_counts.items()):
            percentage = (count / total_students) * 100 if total_students > 0 else 0
            result.append({
                'grade': grade,
                'count': count,
                'percentage': percentage
            })
        
        return result
    
    @staticmethod
    def calculate_pass_rate(students):
        """
        Calculate pass rate (assuming CGPA >= 2.0 is passing)
        """
        if not students:
            return 0.0
        
        passed = sum(1 for student in students if student.cgpa >= 2.0)
        pass_rate = (passed / len(students)) * 100
        
        return pass_rate
    
    @staticmethod
    def perform_analysis(students, analysis_type):
        """
        Perform statistical analysis on student data
        
        Args:
            students: List of student objects
            analysis_type: Type of analysis to perform
        
        Returns:
            Dictionary with analysis results and processing time
        """
        start_time = time.time()
        
        result = {
            'faculty_stats': [],
            'grade_distribution': [],
            'pass_rate': 0.0
        }
        
        if analysis_type in ["avg_cgpa_faculty", "all"]:
            result['faculty_stats'] = StatsService.calculate_avg_cgpa_by_faculty(students)
        
        if analysis_type in ["grade_distribution", "all"]:
            result['grade_distribution'] = StatsService.calculate_grade_distribution(students)
        
        if analysis_type in ["pass_rate", "all"]:
            result['pass_rate'] = StatsService.calculate_pass_rate(students)
        
        processing_time = time.time() - start_time
        
        result['processing_time'] = processing_time
        return result
    
    @staticmethod
    def calculate_statistics(students):
        """
        Comprehensive statistical analysis wrapper
        Calculates mean, median, std dev, and distributions
        
        Args:
            students: List of student objects
        
        Returns:
            Dictionary with statistics and processing_time
        """
        start_time = time.time()
        
        if not students:
            return {
                'statistics': {},
                'processing_time': 0.0
            }
        
        # Calculate CGPA statistics
        cgpas = [s.cgpa for s in students]
        cgpas_sorted = sorted(cgpas)
        n = len(cgpas)
        
        mean_cgpa = sum(cgpas) / n
        median_cgpa = cgpas_sorted[n // 2] if n % 2 == 1 else (cgpas_sorted[n // 2 - 1] + cgpas_sorted[n // 2]) / 2
        
        # Standard deviation
        variance = sum((x - mean_cgpa) ** 2 for x in cgpas) / n
        std_dev = variance ** 0.5
        
        # Faculty distribution
        faculty_counts = defaultdict(int)
        for student in students:
            faculty_counts[student.faculty] += 1
        
        # Grade distribution
        grade_counts = defaultdict(int)
        for student in students:
            grade_counts[student.grade] += 1
        
        processing_time = time.time() - start_time
        
        return {
            'statistics': {
                'cgpa': {
                    'mean': mean_cgpa,
                    'median': median_cgpa,
                    'std_dev': std_dev,
                    'min': min(cgpas),
                    'max': max(cgpas)
                },
                'distribution': {
                    'total_students': len(students),
                    'total_faculties': len(faculty_counts),
                    'by_faculty': dict(faculty_counts),
                    'by_grade': dict(grade_counts)
                }
            },
            'processing_time': processing_time
        }
