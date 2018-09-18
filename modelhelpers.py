from basichelpers import *
from sklearn.model_selection import cross_val_predict, StratifiedShuffleSplit, GridSearchCV, RandomizedSearchCV, cross_val_score, train_test_split


from sklearn.metrics import accuracy_score, log_loss
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid, RadiusNeighborsClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV, PassiveAggressiveClassifier, Perceptron, RidgeClassifier, RidgeClassifierCV, SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis

def select_classifier(X, y, n_splits=10, test_size=0.1, random_state=42, show=True):
    classifiers = [
        AdaBoostClassifier(),
        BaggingClassifier(),
        BernoulliNB(),
        CalibratedClassifierCV(),
        DecisionTreeClassifier(),
        ExtraTreeClassifier(),
        GaussianNB(),
        GaussianProcessClassifier(),
        GradientBoostingClassifier(),
        KNeighborsClassifier(),
        LinearDiscriminantAnalysis(),
        LinearSVC(),
        LogisticRegression(),
        LogisticRegressionCV(),
        MLPClassifier(),
        MultinomialNB(),
        NearestCentroid(),
        NuSVC(),
        PassiveAggressiveClassifier(),
        Perceptron(),
        QuadraticDiscriminantAnalysis(),
        RadiusNeighborsClassifier(),
        RandomForestClassifier(),
        RidgeClassifier(),
        RidgeClassifierCV(),
        SGDClassifier(),
        SVC()
    ]
    names = [clf.__class__.__name__ for clf in classifiers]
    cv = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=random_state)
    scores = {}
    for i, (name, clf) in enumerate(zip(names, classifiers)):
        print('Processing {}...'.format(name))
        for train_index, test_index in cv.split(X, y):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            try:
                clf.fit(X_train, y_train)
                train_predictions = clf.predict(X_test)
                acc = accuracy_score(y_test, train_predictions)
            except:
                acc = 0
            s = scores.get(name, [])
            s.append(acc)
            scores[name] = s
    scores = [[n, np.mean(s)] for n, s in scores.items()]
    scores = pd.DataFrame(scores, columns=['Classifier', 'Score']).sort_values(by='Score', ascending=False)
    if show:
        print(scores)
    return scores.iloc[0, 0], classifiers[scores.iloc[0].name], scores


from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, BaggingRegressor, ExtraTreesRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsRegressor
from sklearn.linear_model import HuberRegressor, PassiveAggressiveRegressor, RANSACRegressor, SGDRegressor, TheilSenRegressor, ARDRegression, LinearRegression, LogisticRegression, Lasso, Ridge, ElasticNet
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.cross_decomposition import PLSRegression


def select_regressor(X, y, scoring='neg_mean_squared_error', show=True):
    regressors = [
        AdaBoostRegressor(),
        # ARDRegression(),
        BaggingRegressor(),
        DecisionTreeRegressor(),
        ElasticNet(),
        ExtraTreeRegressor(),
        ExtraTreesRegressor(),
        # GaussianProcessRegressor(),
        GradientBoostingRegressor(),
        HuberRegressor(),
        KNeighborsRegressor(),
        Lasso(),
        LinearRegression(),
        # LogisticRegression(),
        MLPRegressor(),
        PassiveAggressiveRegressor(),
        PLSRegression(),
        # RadiusNeighborsRegressor(),
        RandomForestRegressor(),
        RANSACRegressor(),
        Ridge(),
        SGDRegressor(),
        TheilSenRegressor(),
    ]
    names = [reg.__class__.__name__ for reg in regressors]
    # cv = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=random_state)
    scores = {}
    for i, (name, reg) in enumerate(zip(names, regressors)):
        print('Processing {}...'.format(name))
        ss = cross_val_score(reg, X, y, scoring=scoring, cv=10)
        scores[name] = ss
        # for train_index, test_index in cv.split(X, y):
        #     X_train, X_test = X[train_index], X[test_index]
        #     y_train, y_test = y[train_index], y[test_index]
        #     try:
        #         clf.fit(X_train, y_train)
        #         train_predictions = clf.predict(X_test)
        #         rmse = np.sqrt(mean_squared_error(y_test, train_predictions))
        #     except:
        #         rmse = 0
        #     s = scores.get(name, [])
        #     s.append(acc)
        #     scores[name] = s
    scores = [[n, np.sqrt(-s).mean()] for n, s in scores.items()]
    scores = pd.DataFrame(scores, columns=['Regressor', 'Score']).sort_values(by='Score', ascending=True)
    if show:
        print(scores)
    return scores.iloc[0, 0], regressors[scores.iloc[0].name], scores



def simple_model_scores(model, X_train, y_train, X_test=None, y_test=None):
    print('Model:')
    print(' ', model.__class__.__name__)
    scores = np.sqrt(-cross_val_score(model, X_train, y_train, scoring='neg_mean_squared_error', cv=10))
    print('Cross-Valition score:')
    print(' mean:', scores.mean(), 'std:', scores.std())

    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    print('Train set score:')
    print(' ', rmse)

    if not X_test is None:
        y_pred = model.predict(X_test)
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        print('Test data score:')
        print(' ', test_rmse)

def simple_grid_search_scores(model, params, X_train, y_train, cv=10, scoring='neg_mean_squared_error', verbose=1):
    grid = GridSearchCV(model, params, cv=cv, scoring=scoring, verbose=verbose)
    grid.fit(X_train, y_train)
    print('== Grid Search ================')
    print('Best parameters:')
    print(' ', grid.best_params_)
    return grid

def learning_curve_gen(model, X, y, size=None, step=1, splitter=train_test_split, scorer=mean_squared_error, **kwargs):
    X_train, X_val, y_train, y_val = splitter(X, y, **kwargs)
    train_errors, val_errors = [], []
    if not size:
        size = len(X)
    for m in range(1, size+1, step):
        model.fit(X_train[:m], y_train[:m])
        y_train_predict = model.predict(X_train[:m])
        y_val_predict = model.predict(X_val)
        train_errors.append(scorer(y_train_predict, y_train[:m]))
        val_errors.append(scorer(y_val_predict, y_val))
    return train_errors, val_errors, list(range(1, size, step))