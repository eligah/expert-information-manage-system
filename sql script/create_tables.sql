BEGIN;

 --
-- Create model Adm
--

CREATE TABLE `expert_system_adm` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `adm_name` varchar(40) NOT NULL, `password` varchar(20) NOT NULL);

 --
-- Create model Certificate
--

CREATE TABLE `expert_system_certificate` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `date` date NOT NULL);

 --
-- Create model Contract
--

CREATE TABLE `expert_system_contract` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `phone` varchar(255) NOT NULL, `address` varchar(255) NOT NULL, `email` varchar(255) NOT NULL, `home` varchar (255) NOT NULL, `post_num` varchar(255) NOT NULL);

 --
-- Create model Education
--

CREATE TABLE `expert_system_education` (`Num` varchar(255) NOT NULL PRIMARY KEY, `degree` varchar(255) NOT NULL, `edu` varchar(255) NOT NULL, `pro` varchar(255) NOT NULL);

 --
-- Create model Eval_exp
--

CREATE TABLE `expert_system_eval_exp` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `description` varchar(255) NOT NULL, `task` varchar(255) NOT NULL, `type` varchar(255) NOT NULL, `time` datet ime(6) NOT NULL);

 --
-- Create model Evaluate
--

CREATE TABLE `expert_system_evaluate` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `field` varchar(255) NOT NULL, `other` longtext NOT NULL, `reason` longtext NOT NULL, `status` varchar(255) N OT NULL, `certificate_id` integer NOT NULL);

 --
-- Create model Expert
--

CREATE TABLE `expert_system_expert` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `username` varchar(40) NOT NULL, `password` varchar(20) NOT NULL);

 --
-- Create model Job
--

CREATE TABLE `expert_system_job` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `achievement` longtext NOT NULL, `comp` varchar(255) NOT NULL, `expertise` longtext NOT NULL, `part` bool NOT NULL , `retire` bool NOT NULL, `job` varchar(255) NOT NULL, `time_len` varchar(255) NOT NULL, `title` varchar(255) NOT NULL);

 --
-- Create model Job_exp
--

CREATE TABLE `expert_system_job_exp` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `company` varchar(255) NOT NULL, `job` varchar(255) NOT NULL, `witness` varchar(255) NOT NULL, `start` date NO T NULL, `end` date NOT NULL);

 --
-- Create model Qualification
--

CREATE TABLE `expert_system_qualification` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `num` varchar(255) NOT NULL, `q_name` varchar(255) NOT NULL);

 --
-- Create model Re_company
--

CREATE TABLE `expert_system_re_company` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NOT NULL, `work` bool NOT NULL);


CREATE TABLE `expert_system_re_company_evaluate` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `re_company_id` integer NOT NULL, `evaluate_id` integer NOT NULL);

 --
-- Create model Capacity
--

CREATE TABLE `expert_system_capacity` (`expert_id` integer NOT NULL PRIMARY KEY, `agency` varchar(255) NOT NULL, `birth` date NOT NULL, `image` varchar(255) NOT NULL, `name` varchar(255) NOT NULL, `
politic` varchar(255) NOT NULL, `sex` varchar(255) NOT NULL, `intype` varchar(255) NOT NULL, `type_card` varchar(255) NOT NULL, `card_num` varchar(255) NOT NULL, `contract_id` integer NOT NULL, `edu
cation_id` varchar(255) NOT NULL, `job_id` integer NOT NULL);

 --
-- Add field capacity to qualification
--

ALTER TABLE `expert_system_qualification` ADD COLUMN `capacity_id` integer NOT NULL;


ALTER TABLE `expert_system_qualification`
ALTER COLUMN `capacity_id`
DROP DEFAULT;

 --
-- Add field capacity to job_exp
--

ALTER TABLE `expert_system_job_exp` ADD COLUMN `capacity_id` integer NOT NULL;


ALTER TABLE `expert_system_job_exp`
ALTER COLUMN `capacity_id`
DROP DEFAULT;

 --
-- Add field capacity to evaluate
--

ALTER TABLE `expert_system_evaluate` ADD COLUMN `capacity_id` integer NOT NULL;


ALTER TABLE `expert_system_evaluate`
ALTER COLUMN `capacity_id`
DROP DEFAULT;

 --
-- Add field capacity to eval_exp
--

ALTER TABLE `expert_system_eval_exp` ADD COLUMN `capacity_id` integer NOT NULL;


ALTER TABLE `expert_system_eval_exp`
ALTER COLUMN `capacity_id`
DROP DEFAULT;


ALTER TABLE `expert_system_evaluate` ADD CONSTRAINT `expert_s_certificate_id_13e823f4_fk_expert_system_certificate_id` FOREIGN KEY (`certificate_id`) REFERENCES `expert_system_certificate` (`id`);
ALTER TABLE `expert_system_re_company_evaluate` ADD CONSTRAINT `expert_sys_re_company_id_26550d78_fk_expert_system_re_company_id` FOREIGN KEY (`re_company_id`) REFERENCES `expert_system_re_company`
(`id`);
ALTER TABLE `expert_system_re_company_evaluate` ADD CONSTRAINT `expert_system__evaluate_id_f00339ba_fk_expert_system_evaluate_id` FOREIGN KEY (`evaluate_id`) REFERENCES `expert_system_evaluate` (`id `);
ALTER TABLE `expert_system_re_company_evaluate` ADD CONSTRAINT `expert_system_re_company_evaluate_re_company_id_68805fa2_uniq` UNIQUE (`re_company_id`, `evaluate_id`);
ALTER TABLE `expert_system_capacity` ADD CONSTRAINT `expert_system_capa_expert_id_319537d5_fk_expert_system_expert_id` FOREIGN KEY (`expert_id`) REFERENCES `expert_system_expert` (`id`);
ALTER TABLE `expert_system_capacity` ADD CONSTRAINT `expert_system__contract_id_e3ed49b3_fk_expert_system_contract_id` FOREIGN KEY (`contract_id`) REFERENCES `expert_system_contract` (`id`);
ALTER TABLE `expert_system_capacity` ADD CONSTRAINT `expert_syst_education_id_b8eeec03_fk_expert_system_education_Num` FOREIGN KEY (`education_id`) REFERENCES `expert_system_education` (`Num`);
ALTER TABLE `expert_system_capacity` ADD CONSTRAINT `expert_system_capacity_job_id_16ab14d5_fk_expert_system_job_id` FOREIGN KEY (`job_id`) REFERENCES `expert_system_job` (`id`);
CREATE INDEX `expert_system_qualification_e89ce398` ON `expert_system_qualification` (`capacity_id`);
ALTER TABLE `expert_system_qualification` ADD CONSTRAINT `expert__capacity_id_ec498d90_fk_expert_system_capacity_expert_id` FOREIGN KEY (`capacity_id`) REFERENCES `expert_system_capacity` (`expert_i d`);
CREATE INDEX `expert_system_job_exp_e89ce398` ON `expert_system_job_exp` (`capacity_id`);
ALTER TABLE `expert_system_job_exp` ADD CONSTRAINT `expert__capacity_id_d25c902e_fk_expert_system_capacity_expert_id` FOREIGN KEY (`capacity_id`) REFERENCES `expert_system_capacity` (`expert_id`);
CREATE INDEX `expert_system_evaluate_e89ce398` ON `expert_system_evaluate` (`capacity_id`);
ALTER TABLE `expert_system_evaluate` ADD CONSTRAINT `expert__capacity_id_32e61e7f_fk_expert_system_capacity_expert_id` FOREIGN KEY (`capacity_id`) REFERENCES `expert_system_capacity` (`expert_id`);
CREATE INDEX `expert_system_eval_exp_e89ce398` ON `expert_system_eval_exp` (`capacity_id`);
ALTER TABLE `expert_system_eval_exp` ADD CONSTRAINT `expert__capacity_id_9e3b76d5_fk_expert_system_capacity_expert_id` FOREIGN KEY (`capacity_id`) REFERENCES `expert_system_capacity` (`expert_id`);
