#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File name: data.py
# Author: Meen Kim
# Date created: 11/11/2017
# Python version: 3.6.1

import sqlite3, time


dname = 'data'
fname = 'openmrs.db'

con = sqlite3.connect('/'.join([dname, fname]))
with con:
	cur = con.cursor()

	# Exercise 1 - 1: provide a list male patients
	query = 'SELECT * FROM patient WHERE gender=\'M\';'
	cur.execute(query);
	male_patients = cur.fetchall()
	print(male_patients)

	# Exercise 1 - 2: provide the counts of patients by gender
	query = 'SELECT gender, COUNT(*) FROM patient GROUP BY gender;'
	cur.execute(query);
	gender_counts = cur.fetchall()
	print(gender_counts)

	# Exercise 2: Count patients diagnosed with DERMITITIS at an encounter
	query = [
		'SELECT DISTINCT e.patient_id', 
		'FROM encounter AS e',
		'INNER JOIN encounter_diagnosis AS ed',
		'ON e.id = ed.encounter_id',
		'INNER JOIN diagnosis AS d',
		'ON ed.diagnosis_id = d.id',
		'WHERE d.name = \'DERMATITIS\';'
	]
	cur.execute(' '.join(query))
	patient_ids = cur.fetchall()
	print(len(patient_ids))

	# Exercise 3: Provide a list patients, by MRN, who have had a CD4 count of less than 300
	query = [
		'SELECT DISTINCT p.mrn', 
		'FROM patient AS p',
		'INNER JOIN encounter AS e',
		'ON p.id = e.patient_id',
		'INNER JOIN lab_result AS l',
		'ON e.id = l.encounter_id',
		'WHERE l.cd4 < 300;'
	]
	cur.execute(' '.join(query))
	patient_mrns = cur.fetchall()
	print(patient_mrns)

	# Exercise 4: Count all female patients above 30 as of today’s date
	query = 'SELECT birthdate FROM patient WHERE gender = \'F\';'
	cur.execute(query);
	birthdates = cur.fetchall()

	now = time.time()
	def is_above_thirty(birthdate):
		epoch = time.mktime(time.strptime(birthdate, '%Y-%m-%d'))
		return (now - epoch) / 60 / 60 / 24 / 365 >= 30

	f = lambda x: is_above_thirty(x[0])

	print(len(list(filter(f, birthdates))))
