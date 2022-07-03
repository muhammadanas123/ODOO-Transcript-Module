# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import date


class CMSTranscript(models.Model):
    _name = 'cms.transcript'

    student_id = fields.Many2one('cms.student')
    student_course_id = fields.One2many('cms.student_course','student_id')
    student_semester_id = fields.One2many("cms.student_semester","student_id")


    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')], 
                             'Status', readonly=True, default="draft")
    
    active = fields.Boolean(default=True)
  




# class CMSTranscriptlines(models.Model):
#     _name = 'cms.transcriptline'
#     # _description = 'Student course Information'

#     name = fields.Many2one('cms.transcript' , required='true')
    

class CMSStudent(models.Model):
    _name = 'cms.student'
    _description = 'Student Information'

    transcript_id = fields.Many2one("cms.transcript")
    student_course_id = fields.One2many('cms.student_course','student_id')
    student_semester_id = fields.One2many("cms.student_semester","student_id")

    # session = fields.Char(compute='_compute_student_session', string='Session', readonly=True)


    name = fields.Char('Student Name', required=True)
    cgpa = fields.Float('Student CGPA', required=True)
    registration_no = fields.Char('Registration No.', required=True)
  
    user_id = fields.Many2one('res.users', string='Responsible', readonly=True, default=lambda self: self.env.user)
    
    date_of_birth = fields.Date('Date of Birth', required=True)
    age = fields.Integer(compute='_compute_student_age', string='Age', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')], 
                             'Status', readonly=True, default="draft")
    
    active = fields.Boolean(default=True)
        
    @api.depends('date_of_birth')
    def _compute_student_age(self):
        '''Method to calculate student age'''
        current_date = date.today()
        for rec in self:
            if rec.date_of_birth:
                start = rec.date_of_birth
                age = (current_date - start).days / 365
                # Age should be greater than 0
                if age > 0.0:
                    rec.age = age
                else:
                    rec.age = 0
            else:
                rec.age = 0

    # @api.depends('student_course_id')
    # def _compute_student_session(self):
    #     '''Method to calculate student age'''
        
    #     for rec in self:
    #         if rec.student_course_id:
    #             session = rec.student_course_id.obtained_marks
                
                # Age should be greater than 0
                
                

    def set_done(self):
        '''Method to change state to done'''
        self.state = 'done'

    def set_cancel(self):
        '''Set the state to draft'''
        self.state = 'cancelled'







class CMSSemester(models.Model):
    _name = 'cms.semester'
    _description = 'Semester Information'

    student_semester_id = fields.One2many("cms.student_semester", "semester_id")
    
    name = fields.Char( string='Name', readonly=True)

    year = fields.Char()
    session = fields.Char()

    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')], 
                             'Status', readonly=True, default="draft")
    
    active = fields.Boolean(default=True)


    # @api.depends('year',"session")
    # def _compute_semester_name(self):
    #     for rec in self:
    #         year = rec.year
    #         session = rec.session
    #         rec.name = year + session




class CMSCourseoffer(models.Model):
    _name = 'cms.course_offer'
    _description = 'Course Information'

    student_course_id = fields.One2many("cms.student_course","student_id")
    name = fields.Char('name', required=True)
    code = fields.Char()
    credit_hrs = fields.Char()
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')], 
                             'Status', readonly=True, default="draft")
    active = fields.Boolean(default=True)



class CMSStudentcourse(models.Model):
    _name = 'cms.student_course'
    _description = 'Student course information'

    transcript_id = fields.Many2one("cms.transcript")
    student_id = fields.Many2one('cms.student', required=True)
    
    courseoffer_id = fields.Many2one('cms.course_offer')

    credit_hours = fields.Char('Credit Hours', required=True)
    obtained_marks = fields.Float('Obtained Marks', required=True)
    total_marks = fields.Float('Total Marks', required=True)
    #grade = fields.Char('Grade', required=True)
    grade_point = fields.Float(compute='_compute_grad_perc', string='Grade Point', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')], 
                             'Status', readonly=True, default="draft")
    active = fields.Boolean(default=True)
    percentage = fields.Float(compute='_compute_grad_perc', string='Percentage', readonly=True)
    grade = fields.Char(compute='_compute_grad_perc', string='Grade', readonly=True)
    


    @api.depends('total_marks','obtained_marks')
    def _compute_grad_perc(self):
        '''Method to calculate '''
        for rec in self:
            if rec.total_marks == 0:
                rec.percentage = 0    
            else:
                rec.percentage = (rec.obtained_marks/ rec.total_marks)*100

            if rec.percentage > 91:
                rec.grade = "A+"
                rec.grade_point = 4
            elif rec.percentage > 86:
                rec.grade = "A"
                rec.grade_point = 4
            elif rec.percentage > 80:
                rec.grade = "B+"
                rec.grade_point = 3.67
            elif rec.percentage > 72:
                rec.grade = "B"
                rec.grade_point = 3.33
            elif rec.percentage > 65:
                rec.grade = "B-"
                rec.grade_point = 2.67
            else:
                rec.grade = "F"
                rec.grade_point = 0

class CMSStudentsemester(models.Model):
    _name = 'cms.student_semester'
    _description = 'Student semester information'

    transcript_id = fields.Many2one("cms.transcript")
    semester_id = fields.Many2one("cms.semester") 
    student_id = fields.Many2one("cms.student")
    sgpa = fields.Float()
    scgpa = fields.Float()

    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')], 
                             'Status', readonly=True, default="draft")
    active = fields.Boolean(default=True)






























# class CMSTranscript(models.Model):
#     _name = 'cms.transcript'
#     _description = 'Student  transcript'

#     name = fields.Char('Semester Info', required=True)

#     gpa = fields.Integer( "GPA", required=True)

#     credit_hrs = fields.Integer("credit hrs")

#     course_type = fields.Char("course type")
    

#     semester =  fields.One2many('cms.student_semester', 'student_id_1', string='course')

#     student_info_id = fields.Many2one('cms.student' , string="semester info" , required='true')


#     state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')], 
#                              'Status', readonly=True, default="draft")

#     active = fields.Boolean(default=True)







