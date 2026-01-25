*** Settings ***
Documentation     Test suite for Employee Facade (Category and Product Management)
Library           ./EmployeeLibrary.py
Test Teardown     Teardown Database

*** Variables ***
${CAT_TITLE}      Electronics
${PROD_TITLE}     Gaming Mouse
*** Test Cases ***

Verify Category Lifecycle
    [Documentation]    Test adding a new category, updating it and then deleting it via Employee Facade.

    # 1. Add Category
    ${cat_id}=    Create Category Via Facade    ${CAT_TITLE}    Description for Electronics
    Category Should Exist    ${CAT_TITLE}

    # 2. Delete Category
    Delete Category Via Facade    ${cat_id}
    Category Should Not Exist    ${CAT_TITLE}

Verify Category Description Update
    [Documentation]    Test that changing description works in DB.

    # 1. Setup
    ${cat_id}=    Create Category Via Facade    Hardware    Original Description

    # 2. Action: Update the Category
    Update Category Via Facade    ${cat_id}    Hardware    Updated Description

    # 3. Verification
    Category Should Have Description    ${cat_id}    Updated Description

Verify Product Lifecycle
    [Documentation]    Test adding a product (requires a category) and deleting it via Employee Facade.

    # 1. Setup: We need a category first because Product requires a Foreign Key
    ${cat_id}=    Create Category Via Facade    Hardware

    # 2. Add Product
    ${prod_id}=   Create Product Via Facade    ${PROD_TITLE}    50.00    ${cat_id}
    Product Should Exist    ${PROD_TITLE}

    # 3. Delete Product
    Delete Product Via Facade    ${prod_id}
    Product Should Not Exist    ${PROD_TITLE}

Verify Product Price Update
    [Documentation]    Test that changing a product's price persists in the DB.

    # 1. Setup
    ${cat_id}=    Create Category Via Facade    Hardware
    ${prod_id}=   Create Product Via Facade    Gaming Mouse    50.00    ${cat_id}

    # 2. Action: Update the product
    # Syntax: Update Product Via Facade  <ID>  <NEW_NAME>  <NEW_PRICE>  <CAT_ID>
    Update Product Via Facade    ${prod_id}    Gaming Mouse    45.00    ${cat_id}

    # 3. Verification
    Product Should Have Price    ${prod_id}    45.00

Attempt To Delete Non-Empty Category
    [Documentation]    Edge Case: Try to delete a category that still has products.

    # 1. Create Category and Product
    ${cat_id}=    Create Category Via Facade    Books
    ${prod_id}=   Create Product Via Facade    Python 101    30.00    ${cat_id}

    # 2. Try to delete the Category
    # Based on your Service code:
    # if is_active_linked (has active products) -> Raise ValueError

    # The '*' matches "ValueError: " or any other prefix
    Run Keyword And Expect Error    *Cannot delete category: It contains active products. Please deactivate products first.    Delete Category Via Facade    ${cat_id}


Verify Bulk Product Creation
    [Documentation]    Happy Path: Create 5 different valid products using a data table.
    ...                The [Template] executes the keyword for every row.
    [Template]         Create And Verify Valid Product
    # Product Name           Price      Category Name
    Logitech G502            250.00     Electronics
    Mechanical Keyboard      400.00     Electronics
    Whiskas Tuna             12.50      Pets
    Cat Scratch Post         89.99      Pets
    Ceramic Coffee Mug       25.00      Home & Living

*** Keywords ***

Create And Verify Valid Product
    [Arguments]    ${prod_name}    ${price}    ${cat_name}

    # 1. Setup: Create the category first (so we have an ID to link to)
    ${cat_id}=    Create Category Via Facade    ${cat_name}

    # 2. Action: Create the product
    ${prod_id}=   Create Product Via Facade    ${prod_name}    ${price}    ${cat_id}

    # 3. Verification: Confirm it is in the database
    Product Should Exist    ${prod_name}
    Product Should Have Price    ${prod_id}    ${price}