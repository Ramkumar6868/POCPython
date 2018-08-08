class FakeController < ApplicationController

  def create
    res = {
      classification: []
    }
    r = Random.new
    params[:files].each do |file|
      res[:classification] << {
        file_id: file[:file_id],
        probability: r.rand(1..99)/100.0
      }
    end
    render json: res
  end

  def index
    render json: {a: "hello"}
  end
end
