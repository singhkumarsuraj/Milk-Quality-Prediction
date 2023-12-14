from flask import Flask,render_template,request,abort
import pandas as pd

df = pd.read_csv(r'C:\Users\atifa\Desktop\milk_quality_prediction_project\Datasets\milknew.csv')

from sklearn.model_selection import train_test_split

from sklearn.utils import resample


x_minority1 = df[df['Grade']=='medium']
x_minority2 = df[df['Grade']=='high']
x_majority = df[df['Grade']=='low']

x_minority1_upsampled = resample(x_minority1,n_samples=374+55,replace=True,random_state=30)

x_minority2_upsampled = resample(x_minority2,n_samples=256+173,replace=True,random_state=30)

df2 = pd.concat([x_minority1_upsampled,x_minority2_upsampled,x_majority])
x = df2.drop(['Grade'],axis=1)
y = df2['Grade']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=45)

from sklearn.neighbors import KNeighborsClassifier
model1 = KNeighborsClassifier()
model1.fit(x_train,y_train)



app=Flask(__name__)


@app.errorhandler(404)
def not_fount_error(e):
    print(e)  
    return render_template("404.html"),404


@app.errorhandler(500)
def not_fount_error(e):

    app.logger.error(f'Server error: {e} , route:{request.url}')  
    return render_template("500.html"),500

@app.route('/')
def home():
    result = ''
    return render_template('info.html',**locals())

@app.route('/predict' , methods = ['GET','POST'])
def predict():
        if request.method == 'POST':
            pH = float(request.form['pH'])
            Temperature = float(request.form['Temperature'])
            Taste = str(request.form['Taste'])
            Odor = str(request.form['Odor'])
            Fat = int(request.form['Fat'])
            Turbidity = str(request.form['Turbidity'])
            Colour = str(request.form['Color'])

            '''pH = request.form.get('pH')
            Temperature = request.form.get('Temperature')
            Taste = request.form.get('Taste')
            Odor = request.form.get('Odor')
            Fat = request.form.get('Fat')
            Turbidity = request.form.get('Turbidity')
            Colour = request.form.get('Color')'''


 # Validate empty fields
            if not pH or not Temperature or not Taste or not Odor or not Fat or not Turbidity or not Colour:
                error_statement = "All the fields should be filled..."
                return render_template("fail.html", error_statement=error_statement)

            # Validate numeric inputs
            valid_taste_options = ['Excellent', 'Great', 'Good', 'Excellent Taste', 'Great Taste', 'Good Taste']
            if Taste in valid_taste_options:
                Taste=1
            else:
                Taste=0

            good_odor_options = ['Good Odor', 'Milky Odor', 'Faint Odor', 'Good', 'Milky', 'Faint', 'Great']
            if Odor in good_odor_options:
                Odor=1
            else:
                Odor=0

            if not (2 <= Fat <= 5):
                Fat=0
            else:
                Fat=1


            valid_turbidity_options = ['High Cloudiness or Highly Opaque', 'Highly Opaque', 'High Cloudiness', 'Cloudy', 'Opaque', 'Turbid']
            if Turbidity in valid_turbidity_options:
                Turbidity=1
            else:
                Turbidity=0

            
            if Colour== 'White':
                Colour=254
            elif Colour == 'Bright White':
                Colour = 254
            elif Colour == 'Yellowish White':
                Colour=245
            elif Colour=='Gray':
                Colour=248
            else:
                Colour=240
                    
            y_pred = [[pH, Temperature, Taste, Odor, Fat, Turbidity , Colour]]
            '''model = milk_model.model()'''
            result = model1.predict(y_pred)
            print(result)
            return render_template('info.html', result=result , pH=pH , Temperature=Temperature , Taste=Taste, Odor=Odor ,Fat=Fat,Turbidity=Turbidity,Colour=Colour )

if __name__=="__main__":
    app.run(debug=True) 