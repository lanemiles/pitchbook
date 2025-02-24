# Anticompetitive Directors README

- [Summary](#i-summary)
- [Downloading & Running the Code](#ii-downloading--running-the-code)
- [Using the Included Anonymized Input Data](#iii-using-the-included-anonymized-input-data)
- [Brief Code Overview](#iv-brief-code-overview)
- [Creating Your Own Input Data](#v-creating-your-own-input-data)

## I. Summary

This document explains how to download and install our code, provides an overview of how it works, and shows how to use the included anonymized input data as well create custom input data.

**Input Data →** We purchased data from Pitchbook covering the companies, investors, and people associated with all North American based companies that have received venture capital or private equity funding. That data comes in a series of CSV files, each exported out of their database. Those CSV files are the inputs to the program.

We are unable to provide the actual input data purchased from Pitchbook as it is proprietary. See Section III for how to replicate our results using our anonymized copy of that data. If you would like to discuss getting access to all or part of the real Pitchbook data, please reach out. As noted below, the anonymized data is *not permitted to be shared*.

**Output Data →** The output of the code is a CSV file, **results.csv**, containing statistics and tables about interlocks in the provided input data. We used that file as our data reference while writing the paper.

## II. Downloading & Running the Code

The codebase is hosted on Github [here](https://github.com/lanemiles/pitchbook_interlocks). You can download a ZIP file of the code from [here](https://github.com/lanemiles/pitchbook_interlocks/archive/refs/heads/main.zip), or you can clone the repository using git. The codebase is entirely written in Python. Once the code is on your computer, open a Terminal window, *cd* into the root of the project, create and load a new virtual environment, and then install all needed dependencies.

```zsh
# 1. Download the code (or do so manually)
git clone https://github.com/lanemiles/pitchbook_interlocks.git

# 2. Then, setup the project
cd pitchbook_interlocks
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Next, validate the install
python -m pitchbook_interlocks.main --validate
```

The code will always look in the *input\_data* folder for the input CSVs. As discussed more below, you can either use the anonymized input data files that are provided, or you can attempt to create your own versions of the CSVs.  To kick off the actual analysis (which will write to **results.csv**), run:

```zsh
# Run the analysis. Loads input data from the input_data folder. Errors if data is missing.
python -m pitchbook_interlocks.main
```

Note: If one or more of the needed CSVs is missing from the input\_data folder, the code will fail and report which files are missing. 

## III. Using the Included Anonymized Input Data

Note: The anonymized input data may not be shared. Please reach out if you have any questions about this data.

Because the Pitchbook input data is proprietary and cannot be shared, we also provide—for reviewer’s eyes only—a fully anonymized version of that dataset. This anonymized dataset contains exactly the same entities and relationships as the original version, but has all identifying attributes (e.g. names) anonymized.

To install and setup the anonymized input data, run:

```zsh
# 4. Install and setup anonymized input data
python -m pitchbook_interlocks.main --setup-anonymized-input-data
```

The anonymized dataset can be downloaded from [here](https://drive.google.com/file/d/1_brAIQP5gJ08xNMuUl3mhiYJwEk3Fjlo/view?usp=drive_link), if needed. If you download the data manually, you must first copy the provided CSVs into the *input_data* folder. 

After setting up the test data, run *python -m pitchbook_interlocks.main* (the command shown above). 

```zsh
# 5. After setting up the test data, run the analysis
python -m pitchbook_interlocks.main
```

The output will be printed in **results.csv**. We suggest opening that file in Excel or Google Sheets. See Section IV for more details about what is contained in that output CSV.

Some notes on the anonymization:

* ID Fields  
  * All IDs (e.g. CompanyID, PersonID, InvestorID) have been anonymized.  
  * The anonymization is consistent, so each original ID will map to the same anonymized ID in all places in the dataset.  
  * Following Pitchbook’s conventions, all Company and Investor IDs have the same format, while Person IDs have a different format.  
    * Company / Investor ID → ENT-ID-{random digits}  
    * Person ID → PER-ID-{random digits}  
* Name Fields  
  * All Names (e.g. Person Full Name, Investor Name, Company Name) are similarly anonymized.  
  * They all take the form NAME-{random digits}  
* Job Title Fields  
  * Job Titles can be identifying, so all titles are anonymized and take the form TITLE-{random digits}  
  * Note 1: Because of nuance with the loading of Board Observers, we do not anonymize advisory titles of “Advisory Board Member” or “Board Advisor”. These generic labels are not identifying.  
  * Note 2: We report generic Position Levels in the paper, which are derived from each person’s unique job title. Because they are needed for analysis and they are not identifying, we do not anonymize them.  
* Date Fields  
  * All Dates (e.g. PeriodEndDate, StartDate, InvestorSince) have been anonymized. Importantly, the relative ordering of all dates across all files has been kept consistent.  
  * CRITICAL NOTE: The anonymization process keeps dates in their same relative order, but does not necessarily keep the amount of time between two dates constant. As such, if two dates were separated by 10 days before, they could be separated by 2 or 200 days now.   
    * This has one impact on validating the results → The paper cites that the median number of days between an investor’s employee joining the board of a company and the firm investing in that company is 183 days. However, that value is not possible to validate given the anonymous data. Please reach out if this is a significant concern.

## IV. Brief Code Overview

The code operates in two steps. In the “build universe” step, we load the input CSVs, do some data processing, and compute the individual and investor interlocks. In the “print results” step, we print all of our data and statistics to the output CSV.

### Step One: Building the Universe

From the Pitchbook CSVs, we construct the following data entities, with the shown properties and relationships.  

 <img width="982" alt="Screenshot 2025-02-23 at 11 49 42 PM" src="https://github.com/user-attachments/assets/3b31fbca-e703-4956-a85e-76357db9e0d8" />


Next, we identify all individual and investor interlocks. Interlock objects have the schema listed below. 

| Interlock Data Model |  |
| :---: | :---: |
| **Field Name** | **Data Type** |
| Entity ID | String \[Person ID or Investor ID\] |
| Entity Type | String \[PERSON or INVESTOR\] |
| Person 1 ID | String |
| Company 1 ID | String |
| Person 2 ID | String |
| Company 2 ID | String |

### Step Two: Printing the Results

After the universe is built and interlocks are identified, we print out a large amount of data in a CSV file. There are 7 distinct sections in the output CSV. The first section (Paper Tables) contains data for the tables we use in the paper. The following 6 sections contain data that is cited in the paper (e.g. in sentences, not data tables) and additional information for debugging purposes.

| Section Name | Notes |
| :---: | ----- |
| Paper Tables | Purpose-built for the paper, this section contains all of the data for Tables 1-10 in the paper.  |
| Overview Tables | Contains very high-level overview data, like the \# of companies in the universe and the top-line interlock statistics. |
| Company Attributes Tables | Contains breakdowns of interlock frequency and proportion by various company attributes, such as the % of companies in the Healthcare industry with an interlock. It includes breakdowns for the 1+ Board Member, 3+ Board Member, and 5+ Board Member specifications. |
| Individual Interlock Tables | Contains breakdowns of the individual interlocks, like what % of them are attached to people who work at an investor. |
| Investor Interlock Tables | Contains breakdowns of the investor interlocks, such as the frequency and proportions of the various Pitchbook position levels  |
| Appendix Tables | Contains the information necessary to construct the table in Appendix A (industry sub-sector analysis). |
| Interlock Dump Tables | Contains one detailed row for each identified interlock. |

## V. Creating Your Own Input Data

If you would like to create your own version of input data, you are able to do so. For reference, the name and schema of each of the required CSVs is listed below. Note: For several of the less obvious Pitchbook defined fields, the Column Name entry has a link to a PDF of the Pitchbook Help Center article that describes the field, how it is calculated, and its possible values.

Note: This is quite involved and easy to mess up. If you are serious about going down this path, do not hesitate to reach out for support.

### CSV File Schemas

#### 1\. Company.csv

| Column Name | Data Type | Required? | Example Value |
| :---: | :---: | :---: | :---: |
| CompanyID | String | Yes | 342041-14 |
| CompanyName | String | Yes | Rainforest Connection |
| [Business Status](https://drive.google.com/file/d/14DfTeruH36R1usQHWE1KYJzN3SMBkHPF/view?usp=drive_link) | String | No | Generating Revenue |
| [Ownership Status](https://drive.google.com/file/d/12n4Ivs4mHjgAeOH272ybXG8AZ1kZzhoV/view?usp=drive_link) | String | No | Privately Held (backing) |
| [PrimaryIndustrySector](https://drive.google.com/file/d/1DrKT12ZNMdz1QsHKdcZndn-QqdvvK6Bh/view?usp=drive_link) | String | No | Information Technology |
| [PrimaryIndustryGroup](https://drive.google.com/file/d/1DrKT12ZNMdz1QsHKdcZndn-QqdvvK6Bh/view?usp=drive_link) | String | No | Computer Hardware |
| [PrimaryIndustryCode](https://drive.google.com/file/d/1DrKT12ZNMdz1QsHKdcZndn-QqdvvK6Bh/view?usp=drive_link) | String | No | Electronic Equipment and Instruments |
| Revenue | Float | No | 22.6 |
| PeriodEndDate | String | No | 12/31/2023 |

#### 2\. Investor.csv

| Column Name | Data Type | Required? | Example Value |
| :---: | :---: | :---: | :---: |
| InvestorID | String | Yes | 10013-32 |
| InvestorName | String | Yes | Audax Private Equity |

#### 3\. Person.csv

| Column Name | Data Type | Required? | Example Value |
| :---: | :---: | :---: | :---: |
| PersonID | String | Yes | 388659-79P |
| FullName | String | Yes | Alejandra Muguiro |

#### 4\. CompanyCompetitorRelation.csv

| Column Name | Data Type | Required? | Example Value |
| :---: | :---: | :---: | :---: |
| CompanyID | String | Yes | 58691-35 |
| CompetitorID | String | Yes | 146617-12 |

#### 5\. CompanyInvestorRelation.csv

| Column Name | Data Type | Required? | Example Value |
| :---: | :---: | :---: | :---: |
| CompanyID | String | Yes | 58691-35 |
| InvestorID | String | Yes | 10013-32 |
| InvestorSince | String | Yes | 06/11/2021 |

#### 6\. PersonBoardSeatRelation.csv

| Column Name | Data Type | Required? | Example Value |
| :---: | :---: | :---: | :---: |
| PersonID | String | Yes | 58691-35 |
| CompanyID | String | Yes | 10013-32 |
| RoleOnBoard | String | Yes | Board Member |
| IsCurrent | String | Yes | Yes |
| StartDate | String | No | 01/01/2015 |
| EndDate | String | No | 01/01/2020 |

#### 7\. PersonAdvisoryRelation.csv

| Column Name | Data Type | Required? | Example Value |
| :---: | :---: | :---: | :---: |
| PersonID | String | Yes | 58691-35 |
| EntityID | String | Yes | 10013-32 |
| AdvisoryTitle | String | Yes | Advisory Board Member |
| IsCurrent | String | Yes | Yes |
| StartDate | String | No | 01/01/2015 |
| EndDate | String | No | 01/01/2020 |

#### 8\. PersonPositionRelation.csv

| Column Name | Data Type | Required? | Example Value |
| :---: | :---: | :---: | :---: |
| PersonID | String | Yes | 58691-35 |
| EntityID | String | Yes | 10013-32 |
| FullTitle | String | Yes | Partner & Chief Legal Officer |
| [Position Level](https://drive.google.com/file/d/1s9sSaKGg0-b2af8Adt04o4YsTY6nHB0l/view?usp=drive_link) | String | Yes | Partner |
| IsCurrent | String | Yes | Yes |
| StartDate | String | No | 01/01/2015 |
| EndDate | String | No | 01/01/2020 |

### Notes on Creating Your Own Input Data

Some things to keep in mind if you try to create your own test data:

* **Ensure Companies, Investors, and People Are in Their Base Entity CSVs**  
  * You cannot create a new entity in a relational file (e.g. CompanyCompetitorRelation.csv).   
  * For example, if Company A exists in Company.csv, and you add a row in CompanyCompetitorRelation.csv linking Company A with a new Company B, this competitor relationship will fail to be captured until you add Company B to Company.csv as well.  
* **Removing Companies Without Data**  
  * We remove all companies that have either no board members or no competitors.  
* **Bidirectional Competition**  
  * We treat all competitor relationships as bidirectional, so a row of \[Company A, Company B\] in CompanyCompetitorRelation.csv will lead to both companies being deemed as competitors with each other  
* **Required IsCurrent \= Yes**  
  * For Board Seats (via PersonBoardSeatRelation.csv and PersonAdvisoryRelation.csv) and Employment at Investors (via PersonPositionRelation), we only take rows where IsCurrent \= Yes. That is, we construct the current state of each company’s board and the current state of each investor’s employee base.  
* **Acceptable AdvisoryTitles**  
  * Because we want to include Advisory Board Members, but not generic Advisors to the company, we only take rows from PersonAdvisoryRelation.csv where the AdvisoryTitle is either "Advisory Board Member" or "Board Advisor."  
* **EntityID Varies By CSV File**  
  * For both PersonAdvisoryRelation.csv, and PersonPositionRelation.csv, the tables themselves use EntityID as the column because they include advisors to and employment at Companies, as well as Investors.   
  * We want to know about Board Advisors at Companies, so we treat EntityID as a CompanyID when reading PersonAdvisoryRelation.csv  
  * We want to know about Employment at Investors, so we treat EntityID as an InvestorID when reading PersonPositionRelation.csv

  
