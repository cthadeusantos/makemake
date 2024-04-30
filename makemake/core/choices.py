BUILDING_STATUS_CHOICES = \
    (
        (0, 'ACTIVE'),
        (1, 'INACTIVE'),
        (2, 'SCRAPPED'),
        (3, 'UNDER CONSTRUCTION'),
        (4, 'CLOSED'),
        (5, 'CONCEPTION'),
        (6, 'LOCKED'),
        (7, 'PENDING'),
        (8, 'APPROVED'),
        (9, 'REJECTED'),
    )

PROJECT_STATUS_CHOICES = \
    (
        (0, 'INITIATION'),
        (1, 'PROGRESS'),
        (2, 'LAUNCH'),
        (3, 'EXECUTION'),
        (4, 'CLOSED'),
        (5, 'STAND BY'),
        (6, 'LOCKED'),
        (7, 'STOPPING'),
        (8, 'CANCELED'),
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

CITIES_CHOICES = ((1, 'Acre'),
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