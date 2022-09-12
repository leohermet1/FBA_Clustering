function  PercentileDenseSpace = DynamicPercentileSampling(NormalizedEuclideanDistanceOrFrequency)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Fernando Silva-Lance 2021 %%%%%%%%%%%%%%%%%
%After a sampling and distance calculation through the discrete or
%continuous method, the function test every possible percentile, from 1 to
%100 and computes the difference between distances of the furthest and the most
%centric solution. This difference suggests how close they are to each
%other. A regression is done:
    % x axis: Number of relevant results obtained with the each percentile.
    % y axis: Difference between the distances of the furthest solution and
    % the most centric solution%
  %The equation obtained is then derivated twice to obtain the inflection
  %point because, after that point, distances will tend to increase as it
  %represents the change in concavity.
%Inputs: 
    %NormalizedEuclideanDistanceOrFrequency: Array including the 
    %total distance/frequency values corresponding to each reaction.
%Outputs:
    %Percentile generated by the second derivative.
 
%NOTE: There are commented plots in case the user wants to visualize the
%inflection point.

        %ArrayOriginal              = ArrayOfSolutions;
        NormalizedOriginal = NormalizedEuclideanDistanceOrFrequency;
        Values4Regression  = zeros(100,2);
        for i = 1:100
            %ArrayOfSolutions = ArrayOriginal;
            NormalizedEuclideanDistanceOrFrequency  = NormalizedOriginal ;
            PercentileDenseSpace         = prctile(NormalizedEuclideanDistanceOrFrequency,i);
            columns_relevant_results     = find(NormalizedEuclideanDistanceOrFrequency <= PercentileDenseSpace); 
            
        %8. Create a new array only considering those solutions within the
        % most dense space of solutions
            %ArrayOfSolutions            = ArrayOfSolutions(:,columns_relevant_results);
            NormalizedEuclideanDistanceOrFrequency = NormalizedEuclideanDistanceOrFrequency(columns_relevant_results);
            distanceFurthestCentral         = max(NormalizedEuclideanDistanceOrFrequency) - min(NormalizedEuclideanDistanceOrFrequency);
            Values4Regression(i,1) = length(columns_relevant_results);
            Values4Regression(i,2) = distanceFurthestCentral;
            
        end   
        
          coff                 = polyfit(Values4Regression(:,1),Values4Regression(:,2),3);
          coffDerivative       = polyder(coff);
          coffDerivative2      = polyder(coffDerivative);
          inflectionPoint      = roots(coffDerivative2);
          similarities = zeros(size(Values4Regression,1),1);
          %plot(Values4Regression(:,1),Values4Regression(:,2)); hold on 
          %plot(inflectionPoint,polyval(coff,inflectionPoint),'o');hold off
          
        %Find the number of points that get closer to the number of points
        %generated by the percentile
          for i = 1:size(Values4Regression,1)
              similarities(i,1) = norm(inflectionPoint(1) - Values4Regression(i,1));
          end
          [~,PercentileDenseSpace] = min(similarities);
          
         %Just in case 
          if PercentileDenseSpace < 5 || isnan(PercentileDenseSpace) || PercentileDenseSpace == 100
              PercentileDenseSpace = 45;         
          end
            
        disp(['Percentil used: ' num2str(PercentileDenseSpace)])
end