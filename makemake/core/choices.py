# Workforce: This term refers to the group of people who are employed by a particular organization or in a particular industry.
# Personnel: This term is more general and can refer to both employees and non-employees who are involved in the work of an organization.
# Staff: This term is often used to refer to the administrative or support employees of an organization.
# Crew: This term is often used to refer to a group of people who work together on a specific task or project.
# Internal stakeholders are those who are directly involved in the organization's operations, such as employees, owners, managers, and shareholders. They have a vested interest in the success of the organization and can influence its decisions and outcomes.
# External stakeholders are those who are not directly involved in the organization's operations but who are affected by its activities, such as customers, suppliers, creditors, communities, and the government. They may have a financial, social, or environmental interest in the organization. 
PEOPLE_WORK_CHOICES = (
    (1, 'Personal'),
    (2, 'Workforce'),
    (3, 'Staff'),
    (4, 'Crew'),
    (5, 'Internal stakeholder'),
    (6, 'External stakeholder')
    )

ORIGIN_PRICES_CHOICES = (
    (0, 'None'),
    (1, 'Allocation factor'),
    (2, 'Collected') # is gathered a better word?
)

BUILDING_STATUS_CHOICES = \
    (
        (0, 'Active'),
        (1, 'Inactive'),
        (2, 'Scrapped'),
        (3, 'Under construction'),
        (4, 'Closed'),
        (5, 'Conception'),
        (6, 'Locked'),
        (7, 'Pending'),
        (8, 'Approved'),
        (9, 'Rejected'),
    )

TYPE_COMPOSITION_CHOICES= \
        (
            (1, 'Material'),
            (2, 'Service'),
            (3, 'Material & Service'),
        )

PROJECT_STATUS_CHOICES = \
    (
        (None, '--------'),
        (1, 'Initiation'),
        (2, 'Progress'),
        (3, 'Launch'),
        (4, 'Execution'),
        (5, 'Closed'),
        (6, 'Stand by'),
        (7, 'Stagnant'),
        (8, 'Halted'),
        (9, 'Stopping'),
        (10, 'Cancelled'),
    )


FILE_EXTENSION_CHOICES = \
    (
        (None, '---'),
        (1, 'Autocad - DWG'),     # Autocad file
        (2, 'Autocad - DXF'),     # Autocad file
        (3, 'Adobe PDF'),     # Portable document format file
        (4, 'Word - DOCX'),    # WORD file
        (5, 'Word - DOC'),     # WORD file
        (6, 'EXCEL - XLSX'),    # EXCEL file
        (7, 'EXCEL - XLS'),     # EXCEL file
        (8, 'Text - TXT'),     # Text file
        (9, 'Libreoffice CALC - ODT'),     # LIBREOFFICE CALC file
        (10, 'Libreoffice Write - ODS'),    # LIBREOFFICE file
        (11, 'Powerpoint - PPTX'),   # Powerpoint file
        (12, 'Powerpoint - PPT'),    # Powerpoint file
        (13, 'Image PNG'),    # Portable Network Graphic, a type of raster image file
        (14, 'Image JPG'),    # Joint Photographic Experts Group (JPEG) file
        (15, 'Image JPEG'),   # Joint Photographic Experts Group (JPEG) file
    )

PLACES_CHOICES = ((1, 'Acre'),
                  (2, 'Alagoas'),
                  (3, 'Amapá'),
                  (4, 'Amazonas'),
                  (5, 'Bahia'),
                  (6, 'Ceará'),
                  (7, 'Distrito Federal'),
                  (8, 'Espírito Santo'),
                  (9, 'Goiás'),
                  (10, 'Maranhão'),
                  (11, 'Mato Grosso'),
                  (12, 'Mato Grosso do Sul'),
                  (13, 'Minas Gerais'),
                  (14, 'Pará'),
                  (15, 'Paraíba'),
                  (16, 'Paraná'),
                  (17, 'Pernambuco'),
                  (18, 'Piauí'),
                  (19, 'Rio de Janeiro'),
                  (20, 'Rio Grande do Norte'),
                  (21, 'Rio Grande do Sul'),
                  (22, 'Rondônia'),
                  (23, 'Roraima'),
                  (24, 'Santa Catarina'),
                  (25, 'São Paulo'),
                  (26, 'Sergipe'),
                  (27, 'Tocantins'),
                  )

BUDGETS_DATABASES_CHOICES = (
    ('', '----------'),
    (1, "OWN"),
    (2, 'SINAPI'),
    (3, 'SCO'),
    (4, 'EMOP'),
    )

PRICES_DATABASES_CHOICES = (
    ('', '----------'),
    (1, "NÃO DESONERADO"),
    (2, 'DESONERADO'),
    )


# DOCUMENT STATUS
# Survey stage
# 1. Feasibility Study: This involves assessing whether the project is technically feasible, economically viable, and organizationally and socially acceptable.
# 2. Conceptualization: This is where the initial ideas for the project are explored and refined to determine if they align with the organization's goals and objectives.
# 3. Needs Assessment: This involves identifying and analyzing the needs and requirements that the project aims to address.
# 4. Pre-Initiation: This stage involves activities that precede the formal initiation of the project, such as gathering initial stakeholder input, conducting high-level risk assessments, and outlining broad project goals.
# Development project statuses
# 1. Initiation: This is the stage where the project is conceived, and initial planning and feasibility studies are conducted.
# 2. Planning: In this phase, detailed planning takes place, including defining objectives, scope, resources, schedule, and budget.
# 3. Execution: This is the phase where the actual project work is performed. Tasks are carried out according to the project plan.
# 4. Monitoring and Controlling: Throughout the project, progress is monitored, and adjustments are made to keep the project on track. This includes tracking performance, managing changes, and addressing issues and risks.
# 5. Closure: Once the project objectives are achieved, or the project is terminated for any reason, the closure phase involves finalizing all project activities, documenting lessons learned, and formally closing out the project.

DOCUMENT_STATUS_CHOICES = \
    (
        (None, '--------'),
        (5, 'Feasibility Study'),
        (10, 'Conceptualization'),
        (15, 'Needs Assessment'),
        (20, 'Pre-Initiation'),
        (25, 'Initiation'),
        (30, 'Planning'),
        (35, 'Execution'),
        (40, 'Monitoring and Controlling'),
        (45, 'Closure'),
    )

AGREEMENT_CATEGORIES_CHOICES = \
    (
        (None, '--------'),
        (1, 'Main'),
        (2, 'Addendum'),
        (3, 'Realignment'),
        (4, 'Readjustment'),
    )

UNIT_CHOICES = ((0, "UNKNOWN"),
                (1, "DIMENSIONLESS"),
                (2, "LENGTH"),
                (3, "AREA"),
                (4, "VOLUME"),
                (5, "MASS"),
                (6, "POWER"),
                (7, "FORCE"),
				(8, "ENERGY"),
                (1000,"SET"),
)

PRICE_TYPE_CHOICES = ((False, "Burdened"),
                (True, "Unburdened"),
)
