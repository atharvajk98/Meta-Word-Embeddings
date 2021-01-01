# Class to implement the Decopuled Autoencoder
# File: DAEME.py
# Author: Atharva Kulkarni

from tensorflow.keras.layers import Input, Dense, concatenate
from tensorflow.keras import backend as K
from tensorflow.keras import Model


class DAE():
    """ Class to implement the Decopuled Autoencoder """
    
    def __init__(self, latent_dim, activation, lambda1, lambda2, lambda3, lambda4, lambda5, lambda6):
        """
        @param latent_dim (int): latent_dimension for each autoencoder. Default: 300.
        @ activation (string): type of activation: leaky_relu, paramaterized_leaky_relu, relu, tanh, and sigmoid. Default: leaky_relu.
        @param lambda1 (int): Multiplicaiton factor for computing loss for part1. Default: 1.
        @param lambda2 (int): Multiplicaiton factor for computing loss for part2. Default: 1.
        @param lambda3 (int): Multiplicaiton factor for computing loss for part3. Default: 1.
        @param lambda4 (int): Multiplicaiton factor for computing loss for part4. Default: 1.
        @param lambda5 (int): Multiplicaiton factor for computing loss for part5. Default: 1.
        @param lambda6 (int): Multiplicaiton factor for computing loss for part6. Default: 1.
        """
        self.model = None
        self.encoder = None
        self.latent_dim = latent_dim
        self.activation = activation
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        self.lambda4 = lambda4
        self.lambda5 = lambda5
        self.lambda6 = lambda6
        
        
        
    def build(self, input_dim):
        """Function to build the decopuled autoencoder.
        @param input_dim (shape): shape of the input dimensions.
        """
        
        def DAE_loss(self, y_true, y_pred):
            """ Function to compute loss for Decopuled Autoencoder.
            @param y_true (np.array): input vector.
            @param y_pred (np.array): output vector.
            @return loss (float): the computed loss
            """    
            return (self.mse(y_true[0], y_pred[0], self.lambda1) + 
                    self.mse(y_true[1], y_pred[1], self.lambda2) + 
                    self.mse(y_true[2], y_pred[2], self.lambda3))
                
                
        input1 = Input(shape=(input_dim,))
        Dense1 = Dense(self.latent_dim, activation=self.activation, name="encoder1")(input1)
        
        input2 = Input(shape=(input_dim,))
        Dense2 = Dense(self.latent_dim, activation=self.activation, name="encoder2")(input2)
        
        input3 = Input(shape=(input_dim,))
        Dense3 = Dense(self.latent_dim, activation=self.activation, name="encoder3")(input3)
        
        bottleneck = concatenate([Dense1, Dense2, Dense3], name="bottleneck")
        
        output1 = Dense(input_dim, activation=self.activation, name="decoder1")(input1)
        output2 = Dense(input_dim, activation=self.activation, name="decoder2")(input2)
        output3 = Dense(input_dim, activation=self.activation, name="decoder3")(input3)
        
        model = Model(inputs=[input1, input2, input3], outputs=[output1, output2, output3])
        encoder = Model(inputs=[input1, input2, input3], outputs=bottleneck)
        model.compile(optimizer="adam", loss=self.DAE_loss)
        model.summary()
        
        return model, encoder
        
        
        
        
     def mse(self, y_true, y_pred, factor):   
        """ Function to compute weighted Mean Squared Error (MSE)
        @param y_true (array): input vector.
        @param y_pred (array): output vector.
        @param factor (float): multiplicative factor.
        @return mse_loss (float): the mean squared error loss.        
        """
        return factor*K.mean(K.square(y_true - y_pred))
        
                    

        