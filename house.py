import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# Load data from CSV file
df = pd.read_csv('Housing.csv')

# Encoding categorical variables
labelencoder = LabelEncoder()
df['mainroad'] = labelencoder.fit_transform(df['mainroad'])
df['guestroom'] = labelencoder.fit_transform(df['guestroom'])
df['basement'] = labelencoder.fit_transform(df['basement'])
df['hotwaterheating'] = labelencoder.fit_transform(df['hotwaterheating'])
df['airconditioning'] = labelencoder.fit_transform(df['airconditioning'])
df['prefarea'] = labelencoder.fit_transform(df['prefarea'])

# Assuming 'furnishingstatus' is the target variable
df['furnishingstatus'] = labelencoder.fit_transform(df['furnishingstatus'])

# Splitting the dataset into the features and target variable
X = df.drop(columns=['price'])
y = df['price']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating a pipeline with standardization and SVR
model = make_pipeline(StandardScaler(), SVR())

# Training the SVR model
model.fit(X_train, y_train)

# Accepting user input for house features
area = float(input("Enter area of the house: "))
bedrooms = int(input("Enter number of bedrooms: "))
bathrooms = int(input("Enter number of bathrooms: "))
stories = int(input("Enter number of stories: "))
mainroad = input("Is the house on the main road? (yes/no): ")
guestroom = input("Does the house have a guest room? (yes/no): ")
basement = input("Does the house have a basement? (yes/no): ")
hotwaterheating = input("Does the house have hot water heating? (yes/no): ")
airconditioning = input("Does the house have air conditioning? (yes/no): ")
parking = int(input("Enter number of parking spots: "))
prefarea = input("Is the house in preferred area? (yes/no): ")
furnishingstatus = input("Enter furnishing status (furnished/semi-furnished/unfurnished): ")

# Mapping user inputs to numeric values
mainroad = 1 if mainroad.lower() == 'yes' else 0
guestroom = 1 if guestroom.lower() == 'yes' else 0
basement = 1 if basement.lower() == 'yes' else 0
hotwaterheating = 1 if hotwaterheating.lower() == 'yes' else 0
airconditioning = 1 if airconditioning.lower() == 'yes' else 0
prefarea = 1 if prefarea.lower() == 'yes' else 0

# Mapping furnishing status to numeric values
furnishingstatus_map = {'furnished': 0, 'semi-furnished': 1, 'unfurnished': 2}
furnishingstatus = furnishingstatus_map.get(furnishingstatus.lower(), -1)  # Default value if not found

if furnishingstatus == -1:
    print("Invalid furnishing status. Please enter 'furnished', 'semi-furnished', or 'unfurnished'.")
else:
    # Predicting the price
    user_input = [[area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea, furnishingstatus]]
    predicted_price = model.predict(user_input)[0]
    print("Predicted price of the house:", predicted_price)
