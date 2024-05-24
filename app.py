from flask import Flask, request, jsonify, session, render_template,flash,redirect,url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('example.db')
    return conn

@app.route('/')
def index():
    return render_template('login.html')  # Render the login form

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('example.db')

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM credentials WHERE username = ?', (username,))
    credential = cursor.fetchone()
    cursor.close(); conn.close()


    if credential is None:
        flash('Invalid username', 'error')
        return redirect(url_for('index'))
    if password != credential[1]:
        flash('Invalid password', 'error')
        return redirect(url_for('index'))
    
    session['username'] = username
    session['isAdmin'] = credential[3]
    session['chefId'] = credential[2]

    if credential[3] == 1:
        return redirect(url_for('admin_logged_in'))
    else:
        return redirect(url_for('chef_logged_in'))


@app.route('/admin_logged_in')
def admin_logged_in():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))
    return render_template('admin_dashboard.html', username=session['username'])

@app.route('/chef_logged_in')
def chef_logged_in():
    if 'username' not in session or session['isAdmin']:
        return redirect(url_for('index'))
    
    chefId = session['chefId']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT recipeName FROM chefs_recipes WHERE chefId = ?', (chefId,))
    recipes = cursor.fetchall()
    print(recipes)
    cursor.close()
    conn.close()
    return render_template('chef_dashboard.html', username=session['username'], recipes=recipes)

@app.route('/edit_cooking_or_pastry/<recipe_name>', methods=['GET', 'POST'])
def edit_cooking_or_pastry(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  
  
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    print(recipe_name)
    cursor.execute('SELECT cookingORpastry FROM recipes WHERE name = ?', (recipe_name,))
    cookingORpastry = cursor.fetchone()   
    if cookingORpastry is None:
        print("r e c i p e  n o t  f o u n d")
        
    print(cookingORpastry[0])

    return render_template('edit_cooking_or_pastry.html', recipe_name=recipe_name, cookingORpastry=cookingORpastry[0])

@app.route('/change_cooking_or_pastry', methods=['POST'])
def change_cooking_or_pastry():
    if 'username' not in session:
        return redirect(url_for('index'))

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        new_value = request.form['cookingORpastry']
        cursor.execute('UPDATE recipes SET cookingORpastry = ? WHERE name = ?', (new_value, recipe_name))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Recipe updated successfully', 'success')

    
    return redirect(url_for('edit_cooking_or_pastry', recipe_name=recipe_name))



@app.route('/edit_recipe_description/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_description(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  
  
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    print(recipe_name)
    cursor.execute('SELECT shortDescription FROM recipes WHERE name = ?', (recipe_name,))
    description = cursor.fetchone()   
    if description is None:
        print("r e c i p e  n o t  f o u n d")

    return render_template('edit_recipe_description.html', recipe_name=recipe_name, description=description[0])

@app.route('/change_recipe_description', methods=['POST'])
def change_recipe_description():
    if 'username' not in session:
        return redirect(url_for('index'))

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        new_value = request.form['new_description']
        cursor.execute('UPDATE recipes SET shortDescription = ? WHERE name = ?', (new_value, recipe_name))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Recipe description updated successfully', 'success')
        return redirect(url_for('edit_recipe_description', recipe_name=recipe_name))

    flash('Failed to update recipe description', 'error')
    return redirect(url_for('edit_recipe_description', recipe_name=recipe_name))








@app.route('/edit_recipe_difficulty/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_difficulty(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  
  
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    print(recipe_name)
    cursor.execute('SELECT difficulty FROM recipes WHERE name = ?', (recipe_name,))
    difficulty = cursor.fetchone()   
    if difficulty is None:
        print("r e c i p e  n o t  f o u n d")

    return render_template('edit_recipe_difficulty.html', recipe_name=recipe_name, difficulty=difficulty[0])

@app.route('/change_recipe_difficulty', methods=['GET', 'POST'])
def change_recipe_difficulty():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        new_difficulty = int(request.form['new_difficulty'])

        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE recipes SET difficulty = ? WHERE name = ?', (new_difficulty, recipe_name))
        conn.commit()
        cursor.close()
        conn.close()
        # Here you would update your recipe in the database
        flash('Recipe difficulty updated successfully', 'success')

    return redirect(url_for('edit_recipe_difficulty', recipe_name=recipe_name))

    #return render_template('edit_recipe_difficulty.html', recipe_name=recipe_name)













@app.route('/edit_recipe_prep_and_cooking_time/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_prep_and_cooking_time(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  
  
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    print(recipe_name)
    cursor.execute('SELECT prepTime,cookingTime FROM recipes WHERE name = ?', (recipe_name,))
    times = cursor.fetchone() 
    if times is None:
        print("r e c i p e  n o t  f o u n d")
    prep_time = times[0]  
    cooking_time = times[1]

    return render_template('edit_recipe_prep_and_cooking_time.html', recipe_name=recipe_name, prep_time = prep_time, cooking_time = cooking_time)

@app.route('/change_recipe_prep_and_cooking_time', methods=['POST'])
def change_recipe_prep_and_cooking_time():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    new_prep_time = request.form['new_prep_time']
    new_cooking_time = request.form['new_cooking_time']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE recipes SET prepTime = ?, cookingTime = ? WHERE name = ?', (new_prep_time, new_cooking_time, recipe_name))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Preparation and cooking times updated successfully', 'success')
    return redirect(url_for('edit_recipe_prep_and_cooking_time', recipe_name=recipe_name))











@app.route('/edit_recipe_national_cuisine/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_national_cuisine(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  
  
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM nationalCuisines')
    national_cuisines = [x[0] for x in cursor.fetchall()]
    cursor.execute('SELECT nationalCuisine FROM recipes WHERE name = ?', (recipe_name,))
    recipe_national_cuisine = cursor.fetchone()
    recipe_national_cuisine = recipe_national_cuisine[0]
    if recipe_national_cuisine is None:
        print("r e c i p e  n o t  f o u n d")


    return render_template('edit_recipe_national_cuisine.html', recipe_name=recipe_name, national_cuisines = national_cuisines, recipe_national_cuisine = recipe_national_cuisine)


@app.route('/change_recipe_national_cuisine', methods=['POST'])
def change_recipe_national_cuisine():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    new_national_cuisine = request.form['new_national_cuisine']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE recipes SET nationalCuisine = ? WHERE name = ?', (new_national_cuisine, recipe_name))
    conn.commit()
    cursor.close()
    conn.close()
    flash('National cuisine updated successfully', 'success')
    return redirect(url_for('edit_recipe_national_cuisine', recipe_name=recipe_name))









@app.route('/edit_recipe_meal_types/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_meal_types(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  
  
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM mealTypes')
    all_of_meal_types = [x[0] for x in cursor.fetchall()]
    cursor.execute('SELECT mealTypeName FROM recipes_mealTypes WHERE recipeName = ?', (recipe_name,))
    recipe_meal_types = [x[0] for x in cursor.fetchall()]
    if recipe_meal_types is None:
        print("r e c i p e  n o t  f o u n d")

    return render_template('edit_recipe_meal_types.html', recipe_name=recipe_name, all_of_meal_types =all_of_meal_types, recipe_meal_types =recipe_meal_types)


@app.route('/add_recipe_meal_type', methods=['POST'])
def add_recipe_meal_type():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    new_meal_type = request.form['new_meal_type']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO recipes_mealTypes (recipeName, mealTypeName) VALUES (?, ?)', (recipe_name, new_meal_type))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Meal type added successfully', 'success')
    return redirect(url_for('edit_recipe_meal_types', recipe_name=recipe_name))

@app.route('/remove_recipe_meal_type', methods=['POST'])
def remove_recipe_meal_type():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    meal_type = request.form['meal_type']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recipes_mealTypes WHERE recipeName = ? AND mealTypeName = ?', (recipe_name, meal_type))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Meal type removed successfully', 'success')
    return redirect(url_for('edit_recipe_meal_types', recipe_name=recipe_name))












@app.route('/edit_recipe_usage_tips/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_usage_tips(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  
  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT usageTip FROM recipes_usageTips WHERE recipeName = ?', (recipe_name,))
    recipe_usage_tips = [x[0] for x in cursor.fetchall()]

    if not recipe_usage_tips:
        flash('Recipe not found', 'error')
        return redirect(url_for('chef_logged_in'))

    return render_template('edit_recipe_usage_tips.html', recipe_name=recipe_name, recipe_usage_tips=recipe_usage_tips)

@app.route('/add_recipe_usage_tip', methods=['POST'])
def add_recipe_usage_tip():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    new_usage_tip = request.form['new_usage_tip']
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO recipes_usageTips (recipeName, usageTip) VALUES (?, ?)', (recipe_name, new_usage_tip))
        conn.commit()
        flash('Usage tip added successfully', 'success')
    except sqlite3.IntegrityError as e:
        flash('Usage tip not added. You can only have up to three usage tips per recipe', 'error')
    
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('edit_recipe_usage_tips', recipe_name=recipe_name))

@app.route('/remove_recipe_usage_tip', methods=['POST'])
def remove_recipe_usage_tip():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    usage_tip = request.form['usage_tip']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recipes_usageTips WHERE recipeName = ? AND usageTip = ?', (recipe_name, usage_tip))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Usage tip removed successfully', 'success')
    return redirect(url_for('edit_recipe_usage_tips', recipe_name=recipe_name))














@app.route('/edit_recipe_tools/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_tools(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  
  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name,usage FROM tools')
    all_tools_available = cursor.fetchall()
    cursor.execute('SELECT tools.name, tools.usage FROM recipes_tools INNER JOIN tools ON recipes_tools.toolName = tools.name WHERE recipes_tools.recipeName = ?', (recipe_name,))
    tools_of_recipe = cursor.fetchall()

    return render_template('edit_recipe_tools.html', recipe_name=recipe_name, all_tools_available =all_tools_available,tools_of_recipe =tools_of_recipe)



@app.route('/add_recipe_tool', methods=['POST'])
def add_recipe_tool():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    new_tool = request.form['new_tool']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO recipes_tools (recipeName, toolName) VALUES (?, ?)', (recipe_name, new_tool))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Tool added successfully', 'success')
    return redirect(url_for('edit_recipe_tools', recipe_name=recipe_name))

@app.route('/remove_recipe_tool', methods=['POST'])
def remove_recipe_tool():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    tool_name = request.form['tool_name']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recipes_tools WHERE recipeName = ? AND toolName = ?', (recipe_name, tool_name))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Tool removed successfully', 'success')
    return redirect(url_for('edit_recipe_tools', recipe_name=recipe_name))





@app.route('/edit_recipe_instuctions/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_instructions(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  
  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT instructionStepNumber,instruction FROM recipes_instructions WHERE recipeName = ?', (recipe_name,))
    recipe_instructions = cursor.fetchall()

    return render_template('edit_recipe_instructions.html', recipe_name=recipe_name, recipe_instructions =recipe_instructions)


@app.route('/update_recipe_instructions', methods=['POST'])
def update_recipe_instructions():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']

    conn = get_db_connection()
    cursor = conn.cursor()

    instructions = {key: value for key, value in request.form.items() if key.startswith('instruction_')}
    
    for key, instruction in instructions.items():
        step_number = int(key.split('_')[1])
        cursor.execute('UPDATE recipes_instructions SET instruction = ? WHERE recipeName = ? AND instructionStepNumber = ?', (instruction, recipe_name, step_number))

    conn.commit()
    cursor.close()
    conn.close()
    flash('Instructions updated successfully', 'success')
    return redirect(url_for('edit_recipe_instructions', recipe_name=recipe_name))

@app.route('/delete_last_instruction', methods=['POST'])
def delete_last_instruction():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(instructionStepNumber) FROM recipes_instructions WHERE recipeName = ?', (recipe_name,))
    max_step = cursor.fetchone()[0]
    if max_step:
        cursor.execute('DELETE FROM recipes_instructions WHERE recipeName = ? AND instructionStepNumber = ?', (recipe_name, max_step))
        conn.commit()
    cursor.close()
    conn.close()
    flash('Last step deleted successfully', 'success')
    return redirect(url_for('edit_recipe_instructions', recipe_name=recipe_name))

@app.route('/add_new_instruction', methods=['POST'])
def add_new_instruction():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    new_instruction = request.form['new_instruction']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(instructionStepNumber) FROM recipes_instructions WHERE recipeName = ?', (recipe_name,))
    max_step = cursor.fetchone()[0]
    next_step = max_step + 1 if max_step else 1
    cursor.execute('INSERT INTO recipes_instructions (recipeName, instructionStepNumber, instruction) VALUES (?, ?, ?)', (recipe_name, next_step, new_instruction))
    conn.commit()
    cursor.close()
    conn.close()
    flash('New instruction added successfully', 'success')
    return redirect(url_for('edit_recipe_instructions', recipe_name=recipe_name))




@app.route('/edit_recipe_ingredients/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_ingredients(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT caloriesPerPortion, proteinsPerPortion, carbohydratesPerPortion, fatsPerPortion, sugarsPerPortion FROM recipes WHERE name = ?', (recipe_name,))
    recipe_nutritional_information = cursor.fetchone()

    cursor.execute('SELECT name, unitOfMeasure, foodGroup FROM ingredients WHERE name NOT IN (SELECT ingredientName FROM recipes_ingredients WHERE recipeName = ?)', (recipe_name,))
    available_ingredients = cursor.fetchall()

    cursor.execute('''
        SELECT recipes_ingredients.ingredientName, ingredients.unitOfMeasure, recipes_ingredients.quantity, ingredients.foodGroup 
        FROM recipes_ingredients 
        INNER JOIN ingredients ON recipes_ingredients.ingredientName = ingredients.name 
        WHERE recipes_ingredients.recipeName = ?
    ''', (recipe_name,))
    recipe_ingredients = cursor.fetchall()

    return render_template('edit_recipe_ingredients.html', recipe_name=recipe_name, available_ingredients=available_ingredients, recipe_ingredients=recipe_ingredients, recipe_nutritional_information=recipe_nutritional_information)


@app.route('/add_recipe_ingredient', methods=['POST'])
def add_recipe_ingredient():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    new_ingredient = request.form['new_ingredient']
    new_quantity = request.form['new_quantity']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO recipes_ingredients (recipeName, ingredientName, quantity) VALUES (?, ?, ?)', (recipe_name, new_ingredient, new_quantity))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Ingredient added successfully', 'success')
    return redirect(url_for('edit_recipe_ingredients', recipe_name=recipe_name))

@app.route('/update_recipe_ingredient', methods=['POST'])
def update_recipe_ingredient():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    ingredient_name = request.form['ingredient_name']
    new_quantity = request.form['new_quantity']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE recipes_ingredients SET quantity = ? WHERE recipeName = ? AND ingredientName = ?', (new_quantity, recipe_name, ingredient_name))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Ingredient quantity updated successfully', 'success')
    return redirect(url_for('edit_recipe_ingredients', recipe_name=recipe_name))


@app.route('/delete_recipe_ingredient', methods=['POST'])
def delete_recipe_ingredient():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    ingredient_name = request.form['ingredient_name']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recipes_ingredients WHERE recipeName = ? AND ingredientName = ?', (recipe_name, ingredient_name))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Ingredient deleted successfully', 'success')
    return redirect(url_for('edit_recipe_ingredients', recipe_name=recipe_name))






@app.route('/edit_recipe_portions/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_portions(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT caloriesPerPortion, proteinsPerPortion, carbohydratesPerPortion, fatsPerPortion, sugarsPerPortion FROM recipes WHERE name = ?', (recipe_name,))
    recipe_nutritional_information = cursor.fetchone()

    cursor.execute('SELECT portions FROM recipes WHERE name = ?', (recipe_name,))
    portions = cursor.fetchone()


    return render_template('edit_recipe_portions.html',recipe_name=recipe_name, portions=portions,recipe_nutritional_information=recipe_nutritional_information)



@app.route('/update_recipe_portions', methods=['POST'])
def update_recipe_portions():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    new_portions = request.form['portions']

    if int(new_portions) < 1:
        flash('Portions must be at least 1', 'error')
        return redirect(url_for('edit_recipe_portions', recipe_name=recipe_name))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE recipes SET portions = ? WHERE name = ?', (new_portions, recipe_name))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Portions updated successfully', 'success')
    return redirect(url_for('edit_recipe_portions', recipe_name=recipe_name))









@app.route('/edit_recipe_basic_ingredient/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe_basic_ingredient(recipe_name):
    if 'username' not in session:
        return redirect(url_for('index'))  

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT basicIngredient FROM recipes WHERE name = ?', (recipe_name,))
    basic_ingredient = cursor.fetchone()

    cursor.execute('SELECT categoryBasedOnBasicIngredient FROM recipes WHERE name = ?', (recipe_name,))
    category_based_on_basic_ingredient = cursor.fetchone()

    cursor.execute('SELECT ingredientName FROM recipes_ingredients WHERE recipeName = ?', (recipe_name,))
    recipe_ingredients = cursor.fetchall()


    return render_template('edit_recipe_basic_ingredient.html',recipe_name=recipe_name,basic_ingredient =basic_ingredient,category_based_on_basic_ingredient =category_based_on_basic_ingredient,recipe_ingredients =recipe_ingredients)



@app.route('/update_recipe_basic_ingredient', methods=['POST'])
def update_recipe_basic_ingredient():
    if 'username' not in session:
        return redirect(url_for('index'))

    recipe_name = request.form['recipe_name']
    new_basic_ingredient = request.form['basic_ingredient']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE recipes SET basicIngredient = ? WHERE name = ?', (new_basic_ingredient, recipe_name))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Basic Ingredient updated successfully', 'success')
    return redirect(url_for('edit_recipe_basic_ingredient', recipe_name=recipe_name))










@app.route('/backup_db', methods=['POST'])
def backup_db():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    try:
        backup_path = 'backup_example.db'
        connection = get_db_connection()
        backup_conn = sqlite3.connect(backup_path)
        
        with backup_conn:
            connection.backup(backup_conn)
        
        backup_conn.close()
        connection.close()

        flash('Database backup successful', 'success')
    except Exception as e:
        flash(f'Database backup failed: {str(e)}', 'error')
    
    return redirect(url_for('admin_logged_in'))

@app.route('/restore_db', methods=['POST'])
def restore_db():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    try:
        backup_path = 'backup_example.db'
        connection = get_db_connection()
        backup_conn = sqlite3.connect(backup_path)
        
        with connection:
            backup_conn.backup(connection)
        
        backup_conn.close()
        connection.close()

        flash('Database restore successful', 'success')
    except Exception as e:
        flash(f'Database restore failed: {str(e)}', 'error')
    
    return redirect(url_for('admin_logged_in'))

@app.route('/execute_season', methods=['POST'])
def execute_season():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    season = request.form['season']
    # Your logic to execute the season
    flash(f'Season {season} executed successfully', 'success')
    return redirect(url_for('admin_logged_in'))




@app.route('/view_finished_seasons', methods=['GET'])
def view_finished_seasons():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT episodeYear FROM episodes')
    finished_seasons_years = [x[0] for x in cursor.fetchall()]  
    cursor.close()
    conn.close()
    
    return render_template('view_finished_seasons.html', title='Finished Seasons', seasons=finished_seasons_years )


@app.route('/view_episode/<int:episode_year>/<int:episode_number>')
def view_episode(episode_year, episode_number):
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetching the recipes for the episode
    cursor.execute('''
        SELECT er.episodeYear, er.episodeNumber, er.recipeNumber, er.recipeName, er.recipeNationalCuisine, c.firstName || ' ' || c.lastName AS chefName
        FROM episode_recipes er
        LEFT JOIN chefs c ON er.chefAssignedToRecipeId = c.id
        WHERE er.episodeYear = ? AND er.episodeNumber = ?
    ''', (episode_year, episode_number))
    recipes = cursor.fetchall()

    # Fetching the scores for each recipe by judge
    cursor.execute('''
        SELECT rs.recipeNumber, rs.judgeNumber, rs.score, j.firstName || ' ' || j.lastName AS judgeName
        FROM recipe_score rs
        LEFT JOIN chefs j ON rs.judgeId = j.id
        WHERE rs.episodeYear = ? AND rs.episodeNumber = ?
    ''', (episode_year, episode_number))
    scores = cursor.fetchall()
    
    cursor.close()
    conn.close()

    if not recipes:
        flash('No recipes found for this episode', 'error')
        return redirect(url_for('view_finished_seasons'))

    # Organize the scores by recipe number
    scores_dict = {}
    for score in scores:
        recipe_number, judge_number, score_value, judge_name = score
        if recipe_number not in scores_dict:
            scores_dict[recipe_number] = []
        scores_dict[recipe_number].append((judge_name, score_value))

    return render_template('view_episode.html', episode_year=episode_year, episode_number=episode_number, recipes=recipes, scores=scores_dict)


@app.route('/delete_latest_season', methods=['POST'])
def delete_latest_season():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Find the latest season
    cursor.execute('SELECT MAX(episodeYear) FROM episodes')
    latest_year = cursor.fetchone()[0]

    if latest_year:
        # Delete the latest season
        cursor.execute('DELETE FROM episodes WHERE episodeYear = ?', (latest_year,))
        cursor.execute('DELETE FROM episode_judges WHERE episodeYear = ?', (latest_year,))
        cursor.execute('DELETE FROM episode_recipes WHERE episodeYear = ?', (latest_year,))
        cursor.execute('DELETE FROM recipe_score WHERE episodeYear = ?', (latest_year,))
        conn.commit()
        flash('season of the year ' + str(latest_year) + ' deleted successfully', 'success')
    else:
        flash('No seasons found to delete', 'error')
    
    cursor.close()
    conn.close()
    
    return redirect(url_for('admin_logged_in'))

@app.route('/create_new_season', methods=['POST'])
def create_new_season():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    with open('create_new_season.py') as f:
        code = f.read()
    exec(code)

    
    flash('New season created successfully', 'success')
    return redirect(url_for('admin_logged_in'))





@app.route('/query_database', methods=['GET'])
def query_database():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))
    return render_template('query_database.html')

@app.route('/query_1', methods=['GET'])
def query_1():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DROP VIEW IF EXISTS view_1;')
    cursor.execute('DROP VIEW IF EXISTS view_2;')
    
    cursor.execute('''
        CREATE VIEW view_1 AS
        SELECT 
            episode_recipes.recipeName,
            episode_recipes.recipeNationalCuisine,
            episode_recipes.chefAssignedToRecipeId,
            recipe_score.score
        FROM 
            recipe_score 
        JOIN 
            episode_recipes ON recipe_score.episodeYear = episode_recipes.episodeYear 
                            AND recipe_score.episodeNumber = episode_recipes.episodeNumber 
                            AND recipe_score.recipeNumber = episode_recipes.recipeNumber;
    ''')
    cursor.execute('''
        CREATE VIEW view_2 AS
        SELECT 
            view_1.recipeName,
            view_1.recipeNationalCuisine,
            chefs.firstName,
            chefs.lastName,
            view_1.score
        FROM 
            view_1
        JOIN 
            chefs ON id = view_1.chefAssignedToRecipeId;
    ''')
    cursor.execute('''
        SELECT 
            firstName || ' ' || lastName AS chefName,
            recipeNationalCuisine,
            AVG(score) AS averageScore
        FROM 
            view_2
        GROUP BY 
            chefName, recipeNationalCuisine
        ORDER BY 
            chefName, recipeNationalCuisine;
    ''')
    results = cursor.fetchall()
    cursor.execute('DROP VIEW view_1;')
    cursor.execute('DROP VIEW view_2;')
    cursor.close()
    conn.close()

    return render_template('query_result.html', results=results, query_name="Μέσος Όρος Αξιολογήσεων (σκορ) ανά μάγειρα και Εθνική κουζίνα")

@app.route('/query_2_form', methods=['GET', 'POST'])
def query_2_form():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT name FROM nationalCuisines')
    national_cuisines = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('SELECT DISTINCT episodeYear FROM episodes')
    years = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return render_template('query_2_form.html', national_cuisines=national_cuisines, years=years)


@app.route('/query_2', methods=['POST'])
def query_2():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    national_cuisine = request.form['national_cuisine']
    year = request.form['year']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query for chefs belonging to the selected national cuisine
    cursor.execute('''
        SELECT chefs.firstName, chefs.lastName
        FROM chefs_nationalCuisines
        JOIN 
            chefs ON chefs_nationalCuisines.chefId = chefs.id
        WHERE chefs_nationalCuisines.nationalCuisineName = ?
    ''', (national_cuisine,))
    chefs_belonging_to_cuisine = cursor.fetchall()

    # Query for chefs who participated in episodes in the selected year
    cursor.execute('''
        SELECT DISTINCT chefs.firstName, chefs.lastName
        FROM episode_recipes
        JOIN chefs ON chefs.id = episode_recipes.chefAssignedToRecipeId
        WHERE episode_recipes.episodeYear = ? AND episode_recipes.recipeNationalCuisine = ?
    ''', (year,national_cuisine))
    chefs_participated_in_year = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('query_2_result.html', 
                           national_cuisine=national_cuisine, 
                           year=year, 
                           chefs_belonging_to_cuisine=chefs_belonging_to_cuisine, 
                           chefs_participated_in_year=chefs_participated_in_year)



@app.route('/query_3', methods=['GET'])
def query_3():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to find young chefs (under 30 years old) with the most recipes
    cursor.execute('''
        SELECT chefs.firstName, chefs.lastName, COUNT(chefs_recipes.chefId) AS recipeCount
        FROM chefs
        JOIN chefs_recipes ON chefs.id = chefs_recipes.chefId
        WHERE (strftime('%Y', 'now') - strftime('%Y', chefs.dateOfBirth)) < 30
        GROUP BY chefs.id
        ORDER BY recipeCount DESC
    ''')
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('query_3_result.html', 
                           results=results, 
                           query_name="Νέοι Μάγειρες (ηλικία < 30 ετών) με τις περισσότερες συνταγές")



@app.route('/query_4', methods=['GET'])
def query_4():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to find chefs who have never participated as judges
    cursor.execute('''
        SELECT c.firstName, c.lastName
        FROM chefs AS c
        LEFT JOIN episode_judges AS ej ON c.id = ej.chefId
        WHERE ej.chefId IS NULL
    ''')
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('query_4_results.html', 
                           results=results, 
                           query_name="Μάγειρες που δεν έχουν συμμετάσχει ποτέ ως κριτές")


@app.route('/query_5', methods=['GET'])
def query_5():
    if 'username' not in session or not session['isAdmin']:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get judges with the same number of appearances in a year with more than three appearances
    cursor.execute('''
        CREATE VIEW view_1 AS
        SELECT chefId, episodeYear, COUNT(*) AS appearances
        FROM episode_judges
        GROUP BY chefId, episodeYear
        HAVING appearances > 1;
    ''')

    cursor.execute('''
        CREATE VIEW view_2 AS
        SELECT t1.chefId AS chefId1, t2.chefId AS chefId2, t1.appearances, t1.episodeYear
        FROM view_1 t1
        JOIN view_1 t2 ON t1.appearances = t2.appearances AND t1.episodeYear = t2.episodeYear
        WHERE t1.chefId < t2.chefId;

    ''')

    cursor.execute('''
        CREATE VIEW view_3 AS
        SELECT 
            c1.firstName AS chef1_firstName, 
            c1.lastName AS chef1_lastName, 
            view_2.chefId2, 
            view_2.appearances, 
            view_2.episodeYear
        FROM view_2
        JOIN chefs c1 ON view_2.chefId1 = c1.id;
    ''')

    cursor.execute('''
        CREATE VIEW view_4 AS
        SELECT 
            view_3.chef1_firstName, 
            view_3.chef1_lastName, 
            c2.firstName AS chef2_firstName, 
            c2.lastName AS chef2_lastName, 
            view_3.appearances, 
            view_3.episodeYear
        FROM view_3
        JOIN chefs c2 ON view_3.chefId2 = c2.id;

    ''')

    cursor.execute('''
        SELECT chef1_firstName, chef1_lastName, chef2_firstName, chef2_lastName, appearances, episodeYear
        FROM view_4
    ''')
    results = cursor.fetchall()

    print(results)

    cursor.execute('DROP VIEW view_1;')
    cursor.execute('DROP VIEW view_2;')
    cursor.execute('DROP VIEW view_3;')
    cursor.execute('DROP VIEW view_4;')
    cursor.close()
    conn.close()

    return render_template('query_5_results.html', 
                           results=results, 
                           query_name="Κριτές με τον ίδιο αριθμό επεισοδίων σε διάστημα ενός έτους με περισσότερες από 3 εμφανίσεις")



@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    return render_template('add_recipe.html')

@app.route('/edit_recipe/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    return render_template('edit_recipe.html', recipe=recipe)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('chefId', None)
    session.pop('isAdmin', None)
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)